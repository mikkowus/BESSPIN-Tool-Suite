#! /usr/bin/env python3
"""  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
This file has the custom numericErrors methods to run tests on qemu|fpga.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # """
import os

from fett.cwesEvaluation.compat import testgenTargetCompatibilityLayer
from fett.base.utils.misc import *

## All tests are assumed to have 1 part except for the following:
partCount = {"test_456" : 3,
             "test_457" : 2,
             "test_665" : 2,
             "test_824" : 2}

class vulClassTester(testgenTargetCompatibilityLayer):
    def __init__(self, target):
        super().__init__(target)
        self.vulClass = "numericErrors"
        return

    def executeTest (self,binTest):
        try:
            testName = binTest.split('.')[0]
            testNum = testName.split('_')[1]
        except Exception as exc:
            self.terminateAndExit (f"executeTest: Failed to parse <{binTest}>.",exc=exc,exitCode=EXIT.Dev_Bug)

        if (isEnabledDict(self.vulClass,'useSelfAssessment')):
            return "\n" + '*'*30 + f" {testName.upper().replace('_',' ')} " + '*'*30 + "\n\n"

        if testName in partCount:
            numParts = partCount [testName]
        else:
            numParts = 1

        outLog = f"<NUMPARTS={numParts}>\n"
        for p in range (numParts):
            # Add "TEST xxx PART P0y" to the log. This is recognized in
            # ./cweScores.py to signal the start of a test part's log
            outLog += f"TEST {testNum} PART P0{p + 1}\n"
            command = f"./{binTest} {p + 1}"
            textBack = self.runCommand (command)[1]
            outLog += textBack
            if (isEnabled('useCustomScoring')): #will need the gdb output here
                outLog += self.getGdbOutput()

        return outLog
