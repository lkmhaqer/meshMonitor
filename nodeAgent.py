#!/usr/bin/python

import urllib2
import datetime
import commands as sp
import re

nodeList = 'https://gist.githubusercontent.com/lkmhaqer/277f1dd1a12dc16f571b/raw/f2cec65ca03395f1e7d95a8ae79ba3fb32057c3d/gistfile1.txt'

def getNodeList():
	try:
		response = urllib2.urlopen(nodeList, timeout = 5)
		content	= response.read()
		localFile = open("nodeList.cfg", 'w')
		localFile.write("# generated " + str(datetime.datetime.now()) + "\n")
		localFile.write(content)
		localFile.close()
		return True;
	except urllib2.URLError as exception:
		return type(exception)

def parseNodeList():
	nodes = [] 
	localFile = open("nodeList.cfg", 'r')
	for line in localFile:
		if '#' not in line:
			nodes.append(line.strip())
	return nodes

def runPing(host):
	summary = []
	returnString = 'Status: '
	status, result = sp.getstatusoutput("ping -c6 -i.2 " + host)
	returnString += str(status) + " | Result: Tx "
	resultArray = result.split('\n')
	for line in resultArray:
		if 'transmitted' in line:
			summary = line.split()
			returnString += summary[0] + " & Rx " + summary[3]
	return returnString

print("Fetching node list..."),
if getNodeList():
	print "Done."

nodeListArray = parseNodeList()

for node in nodeListArray:
	print node + " | " + runPing(node)
