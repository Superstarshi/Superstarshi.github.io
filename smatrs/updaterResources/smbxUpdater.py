import urllib.request
import time

import os

import messagebox

def updateSMBX(filename):
    windowObj.labelString = "Downloading current SMBX patch"

    downloadSMBXPatcher(filename)

    windowObj.loadPercent = 80
    windowObj.labelString = "Running patcher"

    os.startfile(filename)

    windowObj.loadPercent = 90
    windowObj.labelString = "Waiting until patch is complete"

    waitUntilPatchComplete(10,18)

    xtwo = os.path.join(os.getcwd(), "SMBX2.exe")
    rstars = os.path.join(os.getcwd(), "SMATRS Launcher.exe")

    # If the latest patch included an update to the SMBX Launcher itself,
    if os.path.exists(xtwo) and os.path.exists(rstars):
        print("Found SMBX2.exe and SMATRS Launcher.exe")
        windowObj.labelString = "Cleanup pass"

        # Remove the old SMATRS Launcher
        os.remove(rstars)
        print("Removed SMATRS Launcher")

        # ...and rename the new SMBX2.exe to "SMATRS Launcher.exe". The .exe shuffle!
        os.rename(xtwo, rstars)
        print("Renamed SMBX2")
        # ...wait... ".exe"....... thats scary...................

    pass

def waitUntilPatchComplete(querytime, cancelafter=-1):
    time.sleep(querytime)
    if cancelafter == 0:
        print("User got stuck...")
        if messagebox.askyesno("It's been a while...","It seems like it's been a bit of time since the engine updater was launched. If you're stuck, or otherwise had something go wrong, the SMATRS Updater can self-terminate. (If it's still open, this will also close the engine updater!)\n\nDo you want to keep the SMATRS Updater open?"):
            print("...and decided to keep going")
            cancelafter = 9
        else:
            print("...and decided to quit")
            return False

    smbxVer = getModule("universals")['tryLoadSMBXVersion']()

    if smbxVer != getModule("universals")["CLOUD"]["smbx-version"]:
        print(f"Looping; {cancelafter} tries until assuming stuck")
        waitUntilPatchComplete(querytime, cancelafter-1)
    else:
        # Wait for things to settle (might be unnecessary, but not taking risks)
        print(f"Found SMBX game.ini {smbxVer} matching cloud")
        print(f"Waiting {querytime*2} seconds as a safety measure...")

        windowObj.labelString = "Running safety check"

        time.sleep(querytime*2)

        print(f"{querytime*2} seconds have passed; precautionary wait finished")

def downloadSMBXPatcher(filename):
    dlAttempts = 5
    print("Attempting to download patcher from cloud")

    for i in range(dlAttempts):
        try:
            if os.path.exists(filename):
                os.remove(filename)

            urllib.request.urlretrieve(getModule("universals")["filesURL"] + "/patcher.exe", filename)

            print(f"\tCloud SMBX patcher download attempt {i+1}/{dlAttempts} success")
            return
        except Exception as e:
            print(f"\tCloud SMBX patcher download attempt {i+1}/{dlAttempts} failed;\n{e}")
            time.sleep(3 + i**2)

    getModule("universals")["throwError"]("urlError",error="Failed to download SMBX2 patcher")



loadedModules["smbxUpdater"] = {
    'updateSMBX': updateSMBX,
}
