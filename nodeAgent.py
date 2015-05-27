#!/usr/bin/python

import urllib2
import datetime
import commands as sp
import re
import json

nodeList = 'https://gist.githubusercontent.com/lkmhaqer/277f1dd1a12dc16f571b/raw/f2cec65ca03395f1e7d95a8ae79ba3fb32057c3d/gistfile1.txt'
nodeMaster = 'butters.cvn'
nodeSelf = 'butters.cvn'

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
		if 'min/avg/max/mdev' in line:
			pingResult = line.split('/')
			summary.extend([pingResult[4], pingResult[5]])
	summary.append(str(datetime.datetime.now()))
	return summary

print("Fetching node list..."),
if getNodeList():
	print "Done."

nodeListArray = parseNodeList()
localLogFile = open("localICMPLog.log", 'a')
localLogFile.write("    TIME: "  + str(datetime.datetime.now()) + "\n" + "="*42 + "\n")
httpData = []
for node in nodeListArray:
	pingResult = runPing(node)
	httpData.append({'node' : [{'time' : pingResult[5], 'name' : node, 'stat' : pingResult[0], 'tx' : pingResult[1], 'rx' : pingResult[2], 'avg' : pingResult[3], 'max' : pingResult[4]}]})
	localLogFile.write("HOST " + node + "|STAT " + pingResult[0] + "|TX " + pingResult[1] + "|RX " + pingResult[2] + "|AVG " + pingResult[3] + "|MAX " + pingResult[4] + "\n")

localLogFile.close()
request = urllib2.urlopen('http://' + nodeMaster + '/result/' + nodeSelf, json.dumps(httpData))
response = request.read()
request.close()
