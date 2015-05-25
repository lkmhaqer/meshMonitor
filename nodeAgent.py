#!/usr/bin/python

import urllib2
import datetime
import commands as sp
import re

nodeList = 'https://gist.githubusercontent.com/lkmhaqer/277f1dd1a12dc16f571b/raw/f2cec65ca03395f1e7d95a8ae79ba3fb32057c3d/gistfile1.txt'

def getNodeList():
	response = urllib2.urlopen(nodeList, timeout = 5)
	content	= response.read()
	localFile = open("nodeList.cfg", 'w')
	localFile.write("# generated " + str(datetime.datetime.now()) + "\n")
	localFile.write(content)
	localFile.close()
	return True;

def parseNodeList():
	nodes = [] 
	localFile = open("nodeList.cfg", 'r')
	for line in localFile:
		if '#' not in line:
			nodes.append(line.strip())
	return nodes

def runPing(host):
	summary = []
	status, result = sp.getstatusoutput("ping -c6 -i.2 " + host)
	summary.append(str(status))
	resultArray = result.split('\n')
	for line in resultArray:
		if 'transmitted' in line:
			pingResult = line.split()
			summary.extend([pingResult[0], pingResult[3]])
	return summary

print("Fetching node list..."),
if getNodeList():
	print "Done."

nodeListArray = parseNodeList()
localLogFile = open("localICMPLog.log", 'a')
localLogFile.write("    TIME: "  + str(datetime.datetime.now()) + "\n" + "="*42 + "\n")
for node in nodeListArray:
	pingResult = runPing(node);
	localLogFile.write(node + " | Status: " + pingResult[0] + " | PKT TX " + pingResult[1] + " | PKT RX " + pingResult[2] + "\n")

localLogFile.close()
