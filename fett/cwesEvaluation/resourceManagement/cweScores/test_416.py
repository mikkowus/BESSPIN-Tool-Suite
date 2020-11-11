from fett.cwesEvaluation.resourceManagement.cweScores.helpers import *

def test_416 (logTest, testsDir):
    testNum = 416
    if (logTest != "test_{0}.log".format(testNum)):
        return ["CWE-{0}".format(testNum), "--", "Wrong test called!"]
    testLines = readLogLines(logTest, testsDir)

    osImage = getOsImage(testLines, testNum=testNum)

    if (osImage == 'debian' or osImage == 'FreeBSD'):
        nParts = 2
        partsLines = regPartitionTest(testLines, nParts, testNum=testNum)
        partsScores = {}

        for iPart in range(1,nParts+1):
            if (doesKeywordExist(partsLines[iPart],"<INVALID>")):
                partsScores[iPart] = SCORES.CALL_ERR
            elif (doesKeywordExist(partsLines[iPart],'<POINTER_USED_IMPROPERLY>') or doesKeywordExist(partsLines[iPart],'<DOUBLE_FREE_OF_STACK>')):
                partsScores[iPart] = SCORES.V_HIGH
            elif (doesKeywordExist(partsLines[iPart],'Segmentation fault') or doesKeywordExist(partsLines[iPart],'double free detected')):
                partsScores[iPart] = SCORES.HIGH
            else:
                partsScores[iPart] = SCORES.FAIL

    elif (osImage == 'FreeRTOS'):
        nParts = 2
        partsLines = regPartitionTestFreeRTOS(testLines,nParts,testNum=testNum)
        partsScores = {}

        if (doesKeywordExist(partsLines[1], "<ERROR-SIGABRT>")):
            partsScores[1] = SCORES.V_HIGH
        elif (doesKeywordExist(partsLines[1], "<POINTER_USED_IMPROPERLY>")):
            partsScores[1] = SCORES.V_HIGH
        elif (doesKeywordExist(partsLines[1], "<GDB-SIGTRAP>")):
            partsScores[1] = SCORES.V_HIGH
        else:
            partsScores[1] = SCORES.FAIL
        if (doesKeywordExist(partsLines[2], "<ERROR-SIGABRT>")):
            partsScores[2] = SCORES.V_HIGH
        elif (doesKeywordExist(partsLines[2], "<GDB-SIGTRAP>")):
            partsScores[2] = SCORES.V_HIGH
        elif (doesKeywordExist(partsLines[2], "<POINTER_USED_IMPROPERLY>")):
            partsScores[2] = SCORES.V_HIGH
        elif (doesKeywordExist(partsLines[2], "<DOUBLE_FREE_OF_STACK>")):
            partsScores[2] = SCORES.V_HIGH
        else:
            partsScores[2] = SCORES.FAIL

    else:
        print (f"Error: parsing test_{testNum}.log is not implemented for <{osImage}>.")
        return overallScore ([],testNum)

    listScores = [adjustToCustomScore(partsLines[iPart],partsScores[iPart]) for iPart in range(1,nParts+1)]
    return overallScore (listScores ,testNum)