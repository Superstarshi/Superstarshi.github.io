#import subprocess
#import os

#import selfUpdater

#import universals

#universals.tryLoadCloudJSON()

#universals.tryLoadSMBXVersion()

import os
import messagebox

# Modules sytem
global loadedModules, __loadModuleFromContent, getModule

loadedModules = {}

def __loadModuleFromContent(name, content):
    mainGlobals = {
        **globals(),
        "getModule": getModule,
        "loadedModules": loadedModules,
    }
    mainLocals = {}

    exec(content, mainGlobals, mainGlobals)

    return loadedModules[name]

def getModule(name):
    if name in loadedModules:
        return loadedModules[name]

    fullName = f"{resourcesDirectoryPath}\\{name}.py"

    # Check for the internal version of the file
    with open(fullName, "r", encoding="utf-8") as f:
        return __loadModuleFromContent(name, f.read())



if __name__ == "__main__":
    # Run all that's necessary
    # print(updaterDirectoryPath)
    windowObj.loadPercent = 5
    windowObj.labelString = "Loading resources"
    getModule("universals")
    windowObj.loadPercent = 10

    # getModule("selfUpdater")


    if getModule("universals")["versionIsNewer"](getModule("universals")["CLOUD"]["self-updater-version"], getModule("universals")["LOCAL"]["self-updater-version"]):
        # selfUpdater updating
        getModule("selfUpdater")["updateFile"]("selfUpdater")
        # make sure the selfUpdater gets reloaded next time it's ran
        loadedModules.pop("selfUpdater")
        pass

    windowObj.loadPercent = 15

    if getModule("universals")["versionIsNewer"](getModule("universals")["CLOUD"]["smatrs-updater-version"], getModule("universals")["LOCAL"]["smatrs-updater-version"]):
        # smatrsUpdater updating
        windowObj.loadPercent = 20
        getModule("selfUpdater")["updateFile"]("smatrsUpdater")
        pass

    windowObj.loadPercent = 25

    if getModule("universals")["versionIsNewer"](getModule("universals")["CLOUD"]["smbx-version"], getModule("universals")["LOCAL"]["smbx-version"]):
        # smbxUpdater updating
        windowObj.loadPercent = 30
        getModule("selfUpdater")["updateFile"]("smbxUpdater")
        pass

    windowObj.loadPercent = 30
    windowObj.labelString = "Initializing SMATRS update"


    # SMATRS Updater handles checking if it should update for us
    smatrsUpdater = getModule("smatrsUpdater")['SmatrsUpdater']()
    smatrsUpdater.attemptUpdate()

    windowObj.loadPercent = 70
    windowObj.labelString = "Checking SMBX update"

    if getModule("universals")["versionIsNewer"](getModule("universals")["CLOUD"]["smbx-version"], getModule("universals")["LOCAL"]["smbx-version"]):
        # running smbxUpdater
        getModule("smbxUpdater")["updateSMBX"]("patcher.exe")

    windowObj.loadPercent = 100
    windowObj.labelString = "Done!"

    # Done!
    messagebox.showinfo("Way Past Cool!", f"The updater has finished running! If everything was updated correctly, then your installation has been completely updated!\n\nYou can start the game by opening the SMATRS Launcher (or, if it's not there, by opening \"SMBX2\").\n\nHave fun playing!")
