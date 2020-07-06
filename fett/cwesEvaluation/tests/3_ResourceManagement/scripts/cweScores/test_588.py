from .helpers import *

def test_588 (SCORES, customScorer, logTest,testsDir):
    testNum = 588
    if (logTest != "test_{0}.log".format(testNum)):
        return ["CWE-{0}".format(testNum), "--", "Wrong test called!"]
    testLines = readLogLines(logTest,testsDir)

    osImage = getOsImage(testLines,testNum=testNum)

    if (osImage == 'debian' or osImage == 'FreeBSD'):
        nParts = 1
        partsLines = regPartitionTest (testLines,nParts,testNum=testNum)
        partsScores = {}

        partMalRead = partitionLines(testLines,"<struct_pointer_cast_of_scalar_pointer>", "<struct_pointer_cast_of_void_pointer>",testNum=testNum)
        partMalWrite = partitionLines(testLines,"<struct_pointer_cast_of_void_pointer>", "-"*50,testNum=testNum)

        if (doesKeywordExist(testLines,"<INVALID>")):
            partsScores[1] = SCORES.CALL_ERR
        elif (doesKeywordExist(partMalRead,"<ERROR-SEGFAULT>")):
            partsScores[1] = SCORES.V_HIGH
        elif (not doesKeywordExist(partMalRead,"<DEREFERENCE-VIOLATION>")):
            partsScores[1] = SCORES.V_HIGH
        elif (doesKeywordExist(partMalWrite,"<ERROR-SEGFAULT>")):
            partsScores[1] = SCORES.V_HIGH
        elif (not doesKeywordExist(partMalWrite,"<DEREFERENCE-VIOLATION>")):
            partsScores[1] = SCORES.V_HIGH
        else:
            partsScores[1] = SCORES.FAIL

    elif (osImage == 'FreeRTOS'):
        nParts = 2
        partsLines = regPartitionTestFreeRTOS(testLines,nParts,testNum=testNum)
        partsScores = {}

        if (doesKeywordExist(partsLines[1],"<CAST_PASSED_SUCCESSFULLY>")):
            partsScores[1] = SCORES.V_HIGH
        else:
            partsScores[1] = SCORES.V_HIGH
        if (doesKeywordExist(partsLines[2],"<CAST_PASSED_SUCCESSFULLY>")):
            partsScores[2] = SCORES.V_HIGH
        else:
            partsScores[2] = SCORES.V_HIGH


    else:
        print (f"Error: parsing test_{testNum}.log is not implemented for <{osImage}>.")
        return overallScore (SCORES, [],testNum)

    listScores = [customScorer.adjustToCustomScore(partsLines[iPart],partsScores[iPart]) for iPart in range(1,nParts+1)]
    return overallScore (SCORES, listScores ,testNum)