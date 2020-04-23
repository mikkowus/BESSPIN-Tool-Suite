#! /usr/bin/env python3
""" 
Building apps
"""

from fett.base.utils.misc import *
import os

""" The entry function 
---------------------------------------
"""
@decorate.debugWrap
def buildApps ():
    # create the build directory
    buildDir = os.path.join(getSetting('workDir'),'build')
    mkdir(buildDir,addToSettings='buildDir')

    setSetting('sendTarballToTarget',False) #any app has to enable this to send the tarball to target
    tarName = os.path.join(getSetting('buildDir'),getSetting('tarballName'))
    if (isEnabled('buildApps')):
        targetUtilsDir = os.path.join(getSetting('repoDir'),'fett','target','utils')
        cp(os.path.join(targetUtilsDir,'Makefile.xcompileDir'),os.path.join(getSetting('buildDir'),'Makefile'))
        cp(os.path.join(targetUtilsDir,'defaultEnvLinux.mk'),getSetting('buildDir'))

    if (isEnabled('https')):
        buildHttps()
    elif (isEnabled('ota')):
        buildOta()
    elif (isEnabled('webserver')):
        buildWebserver()
    elif (isEnabled('database')):
        buildDatabase(tarName)

"""
- FreeRTOS, building an app means copying the C files/headers/.mk env files to the workDir to prepare for os build.
- Unix: if building is disabled, then nothing to do here. If building is enabled, then we copy and compile here.
"""

# app-specific building steps -----------------------------------------------------------

""" Special building for 'https' """
@decorate.debugWrap
@decorate.timeWrap
def buildHttps():
    pass

""" Special building for 'ota' """
@decorate.debugWrap
@decorate.timeWrap
def buildOta():
    pass

""" Special building for 'webserver' """
@decorate.debugWrap
@decorate.timeWrap
def buildWebserver():
    cpFilesToBuildDir (getSourceDir('webserver'))
    if (isEnabled('buildApps')):
        crossCompileUnix()
    #Create the tarball here to be sent to target
    return

""" Special building for 'database' """
@decorate.debugWrap
@decorate.timeWrap
def buildDatabase(tarName):
    if (isEnabled('buildApps')):
        logAndExit (f"Building from source is not supported for the database application",
                    exitCode=EXIT.Configuration)
    else:
        # Just grab the pre-built binary
        cpFilesToBuildDir (getBinDir('database'), pattern="sqlite")

        # Create the tarball here to be sent to target
        destBin = "sqlite"
        srcBin  = os.path.join(getSetting('buildDir'), "sqlite")
        tar (tarName, filesList=[(destBin, srcBin)])

        setSetting('sendTarballToTarget',True)
    return

# re-used parts -----------------------------------------------------------

@decorate.debugWrap
def getSourceDir (app):
    return os.path.join(getSetting('repoDir'),'fett','apps',app)

@decorate.debugWrap
def getBinDir(app):
    return os.path.join(getSetting('repoDir'),'build', app, getSetting('osImage'))

@decorate.debugWrap
def cpFilesToBuildDir (sourceDir, pattern=None):
    # If no pattern is specified, look for "*.c" files if we're building,
    # otherwise *.riscv
    if pattern is None:
        pattern = "*.c" if isEnabled('buildApps') else "*.riscv"
    cp (sourceDir,getSetting('buildDir'),pattern=pattern)

@decorate.debugWrap
@decorate.timeWrap
def crossCompileUnix():
    #cross-compiling sanity checks
    if ((not isEqSetting('cross-compiler','Clang')) and isEqSetting('linker','LLD')):
        warnAndLog (f"Linking using <{getSetting('linker')}> while cross-compiling with <{getSetting('cross-compiler')} is not supported. Linking using <GCC> instead.>.")
        setSetting('linker','GCC')

    printAndLog (f"Cross-compiling ...")
    envLinux = []
    osImageCap1 = getSetting('osImage')[0].upper() + getSetting('osImage')[1:]
    envLinux.append(f"OS_IMAGE={osImageCap1}")
    envLinux.append(f"TARGET={getSetting('target').upper()}")
    envLinux.append(f"COMPILER={getSetting('cross-compiler').upper()}")
    envLinux.append(f"LINKER={getSetting('linker').upper()}")
    logging.debug(f"going to make using {envLinux}")
    make (envLinux,getSetting('buildDir'))
    printAndLog(f"Files cross-compiled successfully.")




