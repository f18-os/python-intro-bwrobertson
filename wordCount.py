#! /usr/bin/env python3

import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists
import subprocess # executing program
import string

file=input("File Location")

myDic = {}
curFile = open(file).read()
cleanFile = re.sub('[^A-Za-z0-9]+', ' ', curFile)
extraCleanFile = cleanFile.strip(',.').lower()
listFile = extraCleanFile.split()
sortedFile = sorted(listFile)
count = 0
curWord = "a"
for x in range(len(sortedFile)):
    if(curWord==sortedFile[x]):
        count+=1
    else:
        myDic[curWord]=count
        count=1
        curWord=sortedFile[x]

myDic[curWord]=count
with open("myOutput.txt", 'w') as f:
    for key, value in myDic.items():
        f.write('%s %s\n' % (key, value))
