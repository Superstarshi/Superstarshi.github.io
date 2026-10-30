#import subprocess
#import os

#import selfUpdater

#import universals

#universals.tryLoadCloudJSON()

#universals.tryLoadSMBXVersion()

import os
from tkinter import messagebox

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
    getModule("universals")

    # getModule("selfUpdater")


    if getModule("universals")["versionIsNewer"](getModule("universals")["CLOUD"]["self-updater-version"], getModule("universals")["LOCAL"]["self-updater-version"]):
        # selfUpdater updating
        getModule("selfUpdater")["updateFile"]("selfUpdater")
        # make sure the selfUpdater gets reloaded next time it's ran
        loadedModules.pop("selfUpdater")
        pass

    if getModule("universals")["versionIsNewer"](getModule("universals")["CLOUD"]["smatrs-updater-version"], getModule("universals")["LOCAL"]["smatrs-updater-version"]):
        # smatrsUpdater updating
        getModule("selfUpdater")["updateFile"]("smatrsUpdater")
        pass

    if getModule("universals")["versionIsNewer"](getModule("universals")["CLOUD"]["smbx-version"], getModule("universals")["LOCAL"]["smbx-version"]):
        # smbxUpdater updating
        getModule("selfUpdater")["updateFile"]("smbxUpdater")
        pass


    # SMATRS Updater handles checking if it should update for us
    smatrsUpdater = getModule("smatrsUpdater")['SmatrsUpdater']()
    smatrsUpdater.attemptUpdate()

    if getModule("universals")["versionIsNewer"](getModule("universals")["CLOUD"]["smbx-version"], getModule("universals")["LOCAL"]["smbx-version"]):
        # running smbxUpdater
        getModule("smbxUpdater")["updateSMBX"]("patcher.exe")


    # Done!
    messagebox.showinfo("Way Past Cool!", "The updater has finished running! If everything was updated correctly, then your installation has been completely updated!\n\nYou can start the game by opening 'SMBX2.exe'. Have fun playing!")
