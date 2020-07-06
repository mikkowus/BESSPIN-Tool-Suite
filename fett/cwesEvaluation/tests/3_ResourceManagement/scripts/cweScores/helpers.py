#! /usr/bin/env python3
"""  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
helpers functions for scoring the CWE tests
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # """

import re

def readLogLines (logTest,testsDir):
    fLog = open("{0}/{1}".format(testsDir,logTest),"r")
    lines = fLog.read().splitlines()
    fLog.close()
    return lines

def getOsImage (lines,testNum=None):
    warnText = "" if (testNum is None) else " in test_{0}.log".format(testNum)
    for line in lines:
        lineMatch = re.match(r'^<OSIMAGE=(?P<osImage>\w+)>$',line)
        if (lineMatch is not None):
            return lineMatch.group('osImage')
    print ("Error: Could not determine <osImage>{0}.".format(warnText))
    return "NoOsImageFound"

def regPartitionTest (testLines,nParts,testNum=None):
    partsLines = {}
    for iPart in range(1,nParts+1):
        start = f"---Part{iPart:02d}:"
        end = f"---Part{iPart+1:02d}:" if (iPart<nParts) else "-"*50
        partsLines[iPart] = partitionLines(testLines,start,end,testNum=testNum)
    return partsLines

def regPartitionTestFreeRTOS (testLines,nParts,testNum=None):
    partsLines = {}
    for iPart in range(1,nParts+1):
        start = f"---Part{iPart:02d}:"
        end = [f">>>End", "<GDB-SIG", "Error", "error"]
        partsLines[iPart] = partitionLines(testLines,start,end,testNum=testNum)
        #print(partsLines[iPart])
    return partsLines

def partitionLines (lines,start,end,testNum=None):
    warnText = "" if (testNum is None) else " in test_{0}.log".format(testNum)
    startFound = False
    iStart = 0
    isError = False
    iEnd = len(lines)-1
    for iLine,line in enumerate(lines):
        if (start in line):
            if (startFound):
                print ("Warning: part start <{0}> found again{1}.".format(start,warnText))
            startFound = True
            iStart = iLine

        # if (startFound and (end in line)):
        #     iEnd = iLine
        #     return lines[iStart:iEnd+1]
        # if("Error" in line):
        #     lines += ">>>End of Testgen<<<"
        #     return lines[iStart:iEnd+1]
        if (startFound):
            if (isinstance(end,str)): #only one string
                if (end in line):
                    iEnd = iLine
                    return lines[iStart:iEnd+1]
            else:
                for xEnd in end:
                    if (xEnd in line):
                        iEnd = iLine
                        return lines[iStart:iEnd+1]

    if (startFound):
        print ("Warning: part end <{0}> not found{1}.".format(end,warnText))
        return lines[iStart:iEnd+1]   
    else:
        print ("Warning: part start <{0}> not found{1}.".format(start,warnText))
        return []

def overallScore (SCORES, listScores, testNum):
    if (len(listScores)==0): #not implemented
        return ["TEST-{0}".format(testNum), SCORES.NOT_IMPLEMENTED, "Not Implemented"]
    ovrScore = SCORES.minScore(listScores)
    scoreString = ', '.join([f"p{i+1:02d}:{partScore}" for i,partScore in enumerate(listScores)])

    return ["TEST-{0}".format(testNum), ovrScore, scoreString]

def doesKeywordExist (lines, keyword):
    for line in lines:
        if (keyword in line):
            return True
    return False

