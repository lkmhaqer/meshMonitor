#!/usr/bin/python

import urllib2
import datetime
import commands as sp
import re
import json

nodeList	= 'https://gist.githubusercontent.com/lkmhaqer/277f1dd1a12dc16f571b/raw/f2cec65ca03395f1e7d95a8ae79ba3fb32057c3d/gistfile1.txt'
nodeMaster	= 'localhost:5000'
nodeSelf	= 'butters.cvn'
userKey		= '3akhrnb97d3VxwH1xaNWKadfltjoctr476wYgCrAY44O0Dxp'

def fetchHTTP(url, data):
	try:
		request = urllib2.urlopen(url, data)
		response = request.read()
		request.close()
		return response
	except urllib2.HTTPError, e:
		return str(e)

def getNodeList():
	content	= fetchHTTP(nodeList, None)
	localFile = open("listOfNodes.cfg", 'w')
	localFile.write("# generated " + str(datetime.datetime.now()) + "\n")
	localFile.write(content)
	localFile.close()
	return True;

def parseNodeList():
	nodes = [] 
	localFile = open("listOfNodes.cfg", 'r')
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

def writeLog(response, data):
	localLogFile = open("localICMPLog.log", 'a')
	if 'Error' in response:
        	localLogFile.write("    POST: " + response + "\n")
	else:
        	localLogFile.write("    POST: 200\n")
	localLogFile.write("    TIME: "  + str(datetime.datetime.now()) + "\n" + "="*42 + "\n")
	localLogFile.write(str(data) + "\n")
	localLogFile.close()

def getNodeData():
	nodeListArray = parseNodeList()
	data = []
	for node in nodeListArray:
		pingResult = runPing(node)
		data.append({'node' :
					[{'time'  : pingResult[5],
					  'name'  : node,
					  'stat'	: pingResult[0],
					  'tx'	: pingResult[1],
					  'rx'	: pingResult[2],
					  'avg'	: pingResult[3],
					  'max'	: pingResult[4]
					}]
				})
	return data



print("Fetching node list..."),
if getNodeList():
	print("Done.")

httpData = getNodeData() 
response = fetchHTTP('http://' + nodeMaster + '/report/' + userKey + "/" + nodeSelf, json.dumps(httpData))
writeLog(response, httpData)
