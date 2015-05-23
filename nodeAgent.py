#!/usr/bin/python

import urllib2
import datetime

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
	localFile = open("nodeList.cfg", 'r')
	for line in localFile:
		line = line.split('#', 1)[0].strip()
		if not line

print("Fetching node list..."),
if getNodeList():
	print "Done."

