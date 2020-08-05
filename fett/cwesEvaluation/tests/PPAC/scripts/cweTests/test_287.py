import time
import re
import socket, ssl, select

def test_287 (target,binTest):
    testNum = 287
    if (binTest != "test_{0}.riscv".format(testNum)):
        target.reportAndExit ("Error in {0}: Calling <test_{2}> for binary <{1}>.".format(target.filename,binTest,testNum))

    outLog = "\n" + '*'*30 + " TEST {0} ".format(testNum) + '*'*30 + "\n\n"
    outLog += "\n<OSIMAGE={0}>\n".format(target.osImage)

    if (target.osImage == 'debian'):
        if (target.targetObj.isSshConn): #Use the ssh test instead
            outLog += "\n<SSH-TEST>\n"
            def suRoot287 ():
                retLog = ''
                shellRoot = "{0}#".format(target.userName)
                shellUser = '[00m:[01;34m~[00m$'
                isSuccess, textBack, wasTimeout, idxEndsWith = target.runCommand("su root",endsWith=['Password:', shellRoot, shellUser],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False,expectExact=True)
                retLog += textBack
                if (idxEndsWith == 0): #still asks for password
                    retLog += target.runCommand (target.rootPassword,endsWith=shellRoot,showOnScreen=target.showExecutionOnScreen)[1]
                    retLog += "\n<DENIED> su access denied!\n"
                    retLog += target.runCommand ("exit",showOnScreen=target.showExecutionOnScreen)[1]
                elif (idxEndsWith == 1):
                    retLog += "\n<GRANTED> su root access!\n"
                    retLog += target.runCommand("exit",showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
                elif (idxEndsWith == 2): #rejected
                    retLog += "\n<DENIED> su access denied!\n"
                else: #command failed for some reason
                    retLog += "\n<INVALID> Failed to execute <su root>.\n"
                return retLog

            outLog += "-"*20 + "Part01: Vanilla su. Attempt to su root." + "-"*20 + "\n"
            outLog += suRoot287()
            outLog += "-"*60 + "\n\n\n"

            outLog += "-"*20 + "Part02: Expose su. Attempt to su root." + "-"*20 + "\n"

            target.switchUser () #Now on ROOT
            backupCommonAuth = ["cp /etc/pam.d/common-auth /root/common-auth.backup"]
            resetCommonAuth = ["rm /etc/pam.d/common-auth", "mv /root/common-auth.backup /etc/pam.d/common-auth"]
            exposeWithoutAuth = "sed -i \'{0}s:auth.*:auth    sufficient    pam_permit.so:\' {1}" #has to be customized

            retGrep = target.runCommand ("grep -n pam_unix.so /etc/pam.d/common-auth",showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
            outLog += retGrep
            nthLine = -1
            for line in retGrep.splitlines():
                numMatch = re.match(r'^(?P<nthLine>\d+):auth\s+\[success=1 default=ignore\]\s+pam_unix.so\s+nullok_secure$',line)
                if (numMatch is not None):
                    nthLine = numMatch.group('nthLine')
            if (nthLine == -1):
                outLog += "\n Error: Could not find the line number in common-auth.\n"
                return outLog
            outLog += target.runCommand (backupCommonAuth[0],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
            outLog += target.runCommand (exposeWithoutAuth.format(nthLine,"/etc/pam.d/common-auth"),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]

            target.switchUser () #Back on USER
            outLog += suRoot287()
            outLog += "-"*60 + "\n\n\n"

            target.executeOnRoot(resetCommonAuth)

            time.sleep(3)
            return outLog

        def switchUser287 (typeOfSwitch,doPrintResult=True):
            #this method has similar functionality as baseTarget.switchUser, but checks whether linux asks for password, 
            # and whether the switch was successful
            retLog = ''
            shellRoot = ''
            if (typeOfSwitch == 'su'):
                shellRoot = "{0}#".format(target.userName)
            else: #login
                shellRoot = ":~#"
            shellUser = ''
            if (target.backend == "qemu"):
                shellUser = ":~\$" 
            elif (target.backend == "fpga"):
                shellUser = ":~$"
            isGranted = False
            isDenied = False
            msgHeader = typeOfSwitch + ('User' if (target.isCurrentUserRoot) else 'Root')
            if (typeOfSwitch == 'login'):
                retLog += target.runCommand ("exit",endsWith="login:",showOnScreen=target.showExecutionOnScreen)[1]
            useLoginName = target.userName if (target.isCurrentUserRoot) else 'root'
            if (typeOfSwitch == 'login'):
                retCommand = target.runCommand (useLoginName,endsWith=['Password:', shellRoot, shellUser],showOnScreen=target.showExecutionOnScreen)
            else: #su
                retCommand = target.runCommand ("su root",endsWith=['Password:', shellRoot, shellUser],showOnScreen=target.showExecutionOnScreen)
            retLog += retCommand[1]
            if ((not retCommand[0]) or (retCommand[2]) or (retCommand[3] < 0)): #error happened
                target.reportAndExit ("Error in executing test_287. Could not log in again.",overwriteShutdown=True)
                return retLog #never should be executed
            elif (retCommand[3] == 0): #Password is requested
                usePassword = target.userPassword if (target.isCurrentUserRoot) else target.rootPassword
                retLog += target.runCommand (usePassword,endsWith=[shellUser, shellRoot],showOnScreen=target.showExecutionOnScreen)[1]
                #both shells are accepted to work on either su or login
                isDenied = True
                if (typeOfSwitch == 'su'):
                    retLog += target.runCommand ("exit",endsWith=shellUser,showOnScreen=target.showExecutionOnScreen)[1]
            elif (retCommand[3] > 0):
                if (typeOfSwitch == 'login'):
                    if ( ((retCommand[3] == 1) and target.isCurrentUserRoot) or ((retCommand[3] == 2) and not target.isCurrentUserRoot) ):
                        #This would be a surprising state to come to
                        target.reportAndExit ("Error in executing test_287. Interesting state: login with a user name opens the other user shell.")
                        return retLog #never should be executed
                    isGranted = True
                else: #su
                    if (retCommand[3] == 1): #success
                        isGranted = True
                        retLog += target.runCommand ("exit",endsWith=shellUser,showOnScreen=target.showExecutionOnScreen)[1]
                    else:
                        isDenied = True
            if (typeOfSwitch == 'login'):
                target.isCurrentUserRoot = not target.isCurrentUserRoot
            if (doPrintResult):
                if (isGranted):
                    retLog += "\n<{0}-GRANTED>\n".format(msgHeader)
                elif (isDenied):
                    retLog += "\n<{0}-DENIED>\n".format(msgHeader)
                else:
                    retLog += "\n<{0}>\n<INVALID>\n".format(msgHeader)

            return retLog

        #some useful commands
        backupCommonAuth = ["cp /etc/pam.d/common-auth /root/common-auth.backup"]
        resetCommonAuth = ["rm /etc/pam.d/common-auth", "cp /root/common-auth.backup /etc/pam.d/common-auth"]
        cpCommonAuthToUser = "cp /etc/pam.d/common-auth /home/{0}/common-auth.edit".format(target.userName)
        cpCommonAuthToEtc = "cp /home/{0}/common-auth.edit /etc/pam.d/common-auth".format(target.userName)
        exposeToLocalUsers = "sed -i \'{0}s:auth.*:auth    sufficient    pam_localuser.so:\' {1}" #has to be customized
        exposeWithoutAuth = "sed -i \'{0}s:auth.*:auth    sufficient    pam_permit.so:\' {1}" #has to be customized
        checkCommonAuth = "ls -l /etc/pam.d/common-auth"
        rmBackupCommonAuth = ["rm /root/common-auth.backup"]
        rmCommonAuthAtUser = "rm /home/{0}/common-auth.edit".format(target.userName)

        #>>> USER <<<<------------------------------------------------------------
        outLog += target.runCommand("./{0}".format(binTest),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]

        outLog += "-"*20 + "Part01a: Root user allows any local user access." + "-"*20 + "\n"
        target.switchUser () #go to root
        #>>> ROOT <<<<------------------------------------------------------------
        retGrep = target.runCommand ("grep -n pam_unix.so /etc/pam.d/common-auth",showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += retGrep
        nthLine = -1
        for line in retGrep.splitlines():
            numMatch = re.match(r'^(?P<nthLine>\d+):auth\s+\[success=1 default=ignore\]\s+pam_unix.so\s+nullok_secure$',line)
            if (numMatch is not None):
                nthLine = numMatch.group('nthLine')
        if (nthLine == -1):
            outLog += "\n Error: Could not find the line number in common-auth.\n"
            return outLog
        outLog += target.runCommand (backupCommonAuth[0],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (exposeToLocalUsers.format(nthLine,"/etc/pam.d/common-auth"),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]

        outLog += switchUser287('login') #login to user
        #>>> USER <<<<------------------------------------------------------------
        outLog += switchUser287('su') #attempt to su root
        time.sleep(1) #necessary
        outLog += switchUser287('login') #login to root
        #>>> ROOT <<<<------------------------------------------------------------
        if (target.settings['useCustomScoring']): #will need the gdb output here
            outLog += target.getGdbOutput()
        outLog += "-"*60 + "\n\n\n"

        outLog += "-"*20 + "Part01b: Root user removes all authentication requirements." + "-"*20 + "\n"
        outLog += target.runCommand (exposeWithoutAuth.format(nthLine,"/etc/pam.d/common-auth"),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += switchUser287('login') #login to user
        #>>> USER <<<<------------------------------------------------------------
        outLog += switchUser287('su') #attempt to su root
        time.sleep(1) #necessary
        outLog += switchUser287('login') #login to root
        #>>> ROOT <<<<------------------------------------------------------------
        if (target.settings['useCustomScoring']): #will need the gdb output here
            outLog += target.getGdbOutput()
        outLog += "-"*60 + "\n\n\n"

        outLog += target.runCommand (resetCommonAuth[0],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (resetCommonAuth[1],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]

        outLog += "-"*20 + "Part02: common-auth owned by GID=1101" + "-"*20 + "\n"
        addGroup = ["groupadd -g 1101 group_287"]
        addUserToGroup = ["usermod -aG group_287 {0}".format(target.userName)]
        exposeAuthToGrp = ["chgrp group_287 /etc/pam.d/common-auth", "chmod 664 /etc/pam.d/common-auth"]
        target.executeOnRoot (addGroup + addUserToGroup + exposeAuthToGrp)
        target.switchUser ()
        #>>> USER <<<<------------------------------------------------------------
        outLog += target.runCommand(checkCommonAuth,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand("groups",showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        if (target.settings['useCustomScoring']): #will need the gdb output here
            outLog += target.getGdbOutput()
        outLog += "-"*60 + "\n\n\n"

        outLog += "-"*20 + "Part02a: A user from non-root group allow any local user access." + "-"*20 + "\n"
        outLog += target.runCommand (cpCommonAuthToUser,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (exposeToLocalUsers.format(nthLine,"/home/{0}/common-auth.edit".format(target.userName)),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (cpCommonAuthToEtc,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += switchUser287('su') #attempt to su root
        time.sleep(1) #necessary
        outLog += switchUser287('login') #login to root
        #>>> ROOT <<<<------------------------------------------------------------
        time.sleep(1)
        outLog += switchUser287('login') #login to user
        #>>> USER <<<<------------------------------------------------------------
        if (target.settings['useCustomScoring']): #will need the gdb output here
            outLog += target.getGdbOutput()
        outLog += "-"*60 + "\n\n\n"

        outLog += "-"*20 + "Part02b: A user from non-root group removes all authentication requirements." + "-"*20 + "\n"
        outLog += target.runCommand (exposeWithoutAuth.format(nthLine,"/home/{0}/common-auth.edit".format(target.userName)),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (cpCommonAuthToEtc,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += switchUser287('su') #attempt to su root
        time.sleep(1) #necessary
        outLog += switchUser287('login') #login to root
        #>>> ROOT <<<<------------------------------------------------------------
        time.sleep(1)
        outLog += switchUser287('login') #login to user
        #>>> USER <<<<------------------------------------------------------------
        if (target.settings['useCustomScoring']): #will need the gdb output here
            outLog += target.getGdbOutput()
        outLog += "-"*60 + "\n\n\n"

        time.sleep(1) #necessary
        outLog += switchUser287('login') #login to root
        #>>> ROOT <<<<------------------------------------------------------------
        outLog += target.runCommand (resetCommonAuth[0],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (resetCommonAuth[1],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]

        outLog += "-"*20 + "Part03: common-auth accessed by everyone" + "-"*20 + "\n"
        outLog += target.runCommand ("chmod 666 /etc/pam.d/common-auth",showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        target.switchUser ()
        #>>> USER <<<<------------------------------------------------------------
        outLog += target.runCommand(checkCommonAuth,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        if (target.settings['useCustomScoring']): #will need the gdb output here
            outLog += target.getGdbOutput()
        outLog += "-"*60 + "\n\n\n"

        outLog += "-"*20 + "Part03a: A non-root user allows any local user access." + "-"*20 + "\n"
        outLog += target.runCommand ("rm /home/{0}/common-auth.edit".format(target.userName),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (cpCommonAuthToUser,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (exposeToLocalUsers.format(nthLine,"/home/{0}/common-auth.edit".format(target.userName)),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (cpCommonAuthToEtc,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += switchUser287('su') #attempt to su root
        time.sleep(1) #necessary
        outLog += switchUser287('login') #login to root
        #>>> ROOT <<<<------------------------------------------------------------
        time.sleep(1)
        outLog += switchUser287('login') #login to user
        #>>> USER <<<<------------------------------------------------------------
        if (target.settings['useCustomScoring']): #will need the gdb output here
            outLog += target.getGdbOutput()
        outLog += "-"*60 + "\n\n\n"

        outLog += "-"*20 + "Part03b: A non-root user removes all authentication requirements." + "-"*20 + "\n"
        outLog += target.runCommand (exposeWithoutAuth.format(nthLine,"/home/{0}/common-auth.edit".format(target.userName)),showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (cpCommonAuthToEtc,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += switchUser287('su') #attempt to su root
        time.sleep(1) #necessary
        outLog += switchUser287('login') #login to root
        #>>> ROOT <<<<------------------------------------------------------------
        time.sleep(1)
        outLog += switchUser287('login') #login to user
        #>>> USER <<<<------------------------------------------------------------
        if (target.settings['useCustomScoring']): #will need the gdb output here
            outLog += target.getGdbOutput()
        outLog += "-"*60 + "\n\n\n"

        outLog += target.runCommand (rmCommonAuthAtUser,showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += switchUser287('login') #login to root
        #>>> ROOT <<<<------------------------------------------------------------
        outLog += target.runCommand (resetCommonAuth[0],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (resetCommonAuth[1],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
        outLog += target.runCommand (rmBackupCommonAuth[0],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]

        target.switchUser() #has to be logged in as user
        #>>> USER <<<<------------------------------------------------------------
        time.sleep (1)

    elif (target.osImage == 'FreeBSD'):
        def suRoot287 ():
            isSuccess, textBack, wasTimeout, idxEndsWith = target.runCommand("su root",endsWith=["testgenPrompt>",":~ \$",":~ $"],showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)
            if (idxEndsWith == 0):
                retLog = "<GRANTED> su root access!\n"
                retLog += target.runCommand("exit",showOnScreen=target.showExecutionOnScreen,shutdownOnError=False)[1]
            elif (idxEndsWith > 0):
                if ('su: Sorry' in textBack):
                    retLog = "<DENIED> su access denied!\n"
                else:
                    retLog = "<INVALID> Non-recognized response from <su root>."
            else: #command failed for some reason
                retLog = "<INVALID> Failed to execute <su root>."
            return textBack + '\n' + retLog

        backupSu = ["cp /etc/pam.d/su /tmp/su.bak"]
        exposeSu = ["sed -i \"\" \"s/rootok/permit/\" /etc/pam.d/su"]
        resetSu = ["cp /tmp/su.bak /etc/pam.d/su"]
        

        outLog += "-"*20 + "Part01: Vanilla su. Attempt to su root." + "-"*20 + "\n"
        outLog += suRoot287()
        outLog += "-"*60 + "\n\n\n"

        target.executeOnRoot(backupSu + exposeSu)

        outLog += "-"*20 + "Part02: Expose su. Attempt to su root." + "-"*20 + "\n"
        outLog += suRoot287()
        outLog += "-"*60 + "\n\n\n"

        
        target.executeOnRoot(resetSu)
        time.sleep (1)

    elif (target.osImage == 'FreeRTOS'):
        if (target.testsPars['TESTGEN_TEST_PART'] == 1):
            outLog += "-"*20 + "Part01: Valid permissions. List the username." + "-"*20 + "\n"
        elif (target.testsPars['TESTGEN_TEST_PART'] == 2):
            outLog += "-"*20 + "Part02: Valid permissions. Do not list the username." + "-"*20 + "\n"
        elif (target.testsPars['TESTGEN_TEST_PART'] == 3):
            outLog += "-"*20 + "Part03: List the username, do not verify the client." + "-"*20 + "\n"
        elif (target.testsPars['TESTGEN_TEST_PART'] == 4):
            outLog += "-"*20 + "Part04: Do not list the username, receive the actor's name from the connection." + "-"*20 + "\n"
        else:
            outLog += "\n<INVALID> This test has only 4 parts! (called with part #{0})\n".format(target.testsPars['TESTGEN_TEST_PART'])
            return outLog

        socketThreadsCollect = []
        startTime = time.time()
        # start the network
        retCommand = target.activateEthernet ()
        outLog += retCommand[1]
        if ( (not retCommand[0]) or (retCommand[2]) ): #Bad
            outLog += "\n<INVALID> [host]: Failed to ping the target.\n"
            return outLog
        else:
            outLog += "\n[host]: Pinging target successful!\n"

        for i in range(1): #easier construct to break -- loop executed only once
            if (target.testsPars['TESTGEN_TEST_PART'] == 3): #attempt to breach
                message = "Jedi Order CLNT"
                certSuffix = 'SSITH'
            else: #the usual
                message = f"TESTGEN-{testNum}-P0{target.testsPars['TESTGEN_TEST_PART']}.0"
                certSuffix = ''
            try:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.settimeout(60) #blocking operations
                clientSocket.connect((target.ipTarget,target.portTarget))
                #time.sleep(1)
            except:
                outLog += "\n[host-client]: INVALID: Failed to connect to target.\n"
                break
            try:
                TLS_CTX = ssl.SSLContext (ssl.PROTOCOL_TLSv1_2) #create a new context
                TLS_CTX.verify_mode = ssl.CERT_REQUIRED 
                TLS_CTX.load_verify_locations (cafile="{0}/lib/caCert.pem".format(target.testsDir)) #load the CA cert
                TLS_CTX.load_cert_chain(certfile="{0}/lib/clientCert{1}.pem".format(target.testsDir,certSuffix),keyfile="{0}/lib/clientKey{1}.pem".format(target.testsDir,certSuffix))
            except:
                outLog += "\n[host-client]: INVALID: Failed to load the CA certificate into a TLS context.\n"
                break
            try:
                clientSocket = TLS_CTX.wrap_socket(clientSocket,do_handshake_on_connect=True) #wrap the connected socket
                outLog += "\n[host-client]: GRANTED: Socket wrapped successfully!\n"
            except ssl.CertificateError:
                outLog += "\n[host-client]: DENIED: Wrong certificate!\n"
            except socket.timeout:
                outLog += "\n[host-client]: INVALID: Timed-out while trying to wrap the TCP socket.\n"
                break
            except:
                outLog += "\n[host-client]: INVALID: Failed to wrap the TCP socket due to non-CertificateError.\n"
                break    

            try:   
                clientSocket.sendall(message.encode('utf-8'))
            except:
                outLog += "\n<INVALID> [host-client]: Failed to send message to target.\n"
                break
            outLog += target.runCommand("sendToTarget",endsWith="<TARGET-RECV>",erroneousContents="<INVALID>",onlySearchTheEnd=False,timeout=20,shutdownOnError=False)[1]
            try:
                # Look for the response
                ready = select.select([clientSocket], [], [], 10) #10 seconds timeout
                if ready[0]:
                    recvData = str(clientSocket.recv(128),'utf-8')
                    outLog += "\n[host-client]: Received [{0} Bytes]:\n<HOST-RECV>:{1}\n".format(len(recvData),recvData)
                else:
                    raise 
            except:
                outLog += "\n<INVALID> [host-client]: Failed to receive message from target.\n"
                break
            socketThreadsCollect.append(target.socketCloseAndCollect(clientSocket))
            del TLS_CTX
        
        if (">>>End of Testgen<<<" not in outLog):
            retFinish = target.runCommand("allProgram",endsWith=">>>End of Testgen<<<",shutdownOnError=False,timeout=20)
            outLog += retFinish[1]
            if ((not retFinish[0]) or retFinish[2]): #bad
                outLog += "\n<WARNING> Execution did not end properly.\n"
        else: #just to be sure
            outLog += target.readFromTarget() #for anything left
        for xThread in socketThreadsCollect:
            xThread.join(timeout=3)
        minutes, seconds = divmod(time.time()-startTime, 60)
        outLog += "\n\nTest part executed in ~{:0>2}:{:0>2}\n".format(int(minutes),int(seconds))
        outLog += "-"*60 + "\n\n\n"

    else:
        target.reportAndExit("Error in {0}: <test_{2}> is not implemented for <{1}>.".format(target.filename,target.osImage,testNum))
    return outLog