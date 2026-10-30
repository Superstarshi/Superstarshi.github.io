import urllib.request
import time

import os

from tkinter import messagebox

def updateSMBX(filename):
    downloadSMBXPatcher(filename)

    os.startfile(filename)

    waitUntilPatchComplete(10,18)

    if os.path.exists("SMATRS Launcher.exe"):
        os.remove("SMATRS Launcher.exe")

    os.rename("SMBX2.exe", "SMATRS Launcher.exe")

    pass

def waitUntilPatchComplete(querytime, cancelafter=-1):
    time.sleep(querytime)
    if cancelafter == 0:
        if messagebox.askyesno("It's been a while...","It seems like it's been a bit of time since the engine updater was launched. If you're stuck, or otherwise had something go wrong, the SMATRS Updater can self-terminate. (If it's still open, this will also close the engine updater!)\n\nDo you want to keep the SMATRS Updater open?"):
            cancelafter = 9
        else:
            getModule("universals")
            return

    if getModule("universals")['tryLoadSMBXVersion']() != getModule("universals")["CLOUD"]["smbx-version"]:
        print(f"Looping; {cancelafter} tries until assume stuck")
        waitUntilPatchComplete(querytime, cancelafter-1)

def downloadSMBXPatcher(filename):
    for i in range(5):
        try:
            if os.path.exists(filename):
                os.remove(filename)

            urllib.request.urlretrieve(getModule("universals")["filesURL"] + "/patcher.exe", filename)
            # urllib.request.urlretrieve("https://superstarshi.github.io/smatrs/updaterResources/patcher.exe", filename)
            return
        except Exception as e:
            print(f"Cloud SMBX patcher pull attempt {i} failed;\n{e}")
            time.sleep(3 + i**2)

    getModule("universals")["throwError"]("urlError",error="Failed to download SMBX2 patcher")



loadedModules["smbxUpdater"] = {
    'updateSMBX': updateSMBX,
}
