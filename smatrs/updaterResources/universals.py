import os
import sys

from tkinter import messagebox
import urllib.request

import json

import time

import random



# Should be lowercase
validLauncherNames = ["smatrs launcher.exe","smbx2.exe"]
validSaveFilenames = ["progress.json", ".sav","ext.dat"]

versionURL = "https://superstarshi.github.io/smatrs/versioncheck.json"
filesURL = "https://superstarshi.github.io/smatrs/updaterResources"
updateZipFilename = "download.zip"

everythingUpdated = True



episodePath = None
episodeVersion = None
versionName = None

CLOUD = None
LOCAL = None


def versionIsNewer(greaterVersion,lesserVersion):
    "If greaterVersion > lesserVersion, returns True; otherwise returns False"

    digits = max(len(greaterVersion),len(lesserVersion))

    for digitIndex in range(digits):
        digitA = greaterVersion[digitIndex] if digitIndex < len(greaterVersion) else 0
        digitB = lesserVersion[digitIndex] if digitIndex < len(lesserVersion) else 0

        if digitA > digitB:
            return True
        elif digitA < digitB:
            return False
    
    return False


def formatVersion(ver):
    output = "v"

    for i in range(len(ver)):
        output = output + str(ver[i])

        if i < (len(ver) - 1):
            output += "."
    
    return output


def throwError(issue,error = ""):
    errorDict = {
        "errorCode": ["FATAL ERROR!",'Something has gone horribly, horribly wrong.\n\nPlease take a screenshot of this message, join the SMATRS Discord, and request assistance.\n\nThe Updater will close itself after confirmation.\n\nERROR_CODE: ' + error],
        "noEXE": ["Bad Directory!",'The directory the updater is in does not have a file named "SMATRS Launcher.exe" or "SMBX2.exe"!\n\nAre you sure everything is in the right place?'],
        # "smatrsnotfound": ["SMATRS folder not found!",'The data\\worlds\\ directory does not contain any folders titled "SMATRS".\n\nAre you sure everything is in the right place?'],
        "parsingError": ["Parsing Error!","Data could not be properly parsed. Is your installation corrupted?\n\nERROR TRACEBACK: " + error],
        "connectionError": ["Connection Error!","Could not connect to the internet.\n\nIs your wifi working properly?"],
        "urlError": ["URL Error!","URL data could not be properly parsed.\n\nPlease try to run the Updater again. If this persists, please take a screenshot of this message, join the SMATRS Discord, and request assistance.\n\nERROR TRACEBACK: " + error],
        "downloadFail": ["Download Fail!",f"Failed to download SMATRS from cloud! You may be getting rate limited. Please wait a while and try again.\n\nIf the problem persists, please take a screenshot of this message, join the SMATRS Discord, and request assistance."],
        "filenameError": ["Filename Error!",f"An error occured when finding the filename from\n{error}\n\nPlease take a screenshot of this message, join the SMATRS Discord, and request assistance."],
        "unzipError": ["Unzipping Error!",f"An error occured while unzipping the downloaded file at \n{error}\n\nYour save files are safe. They are located in {updaterDirectoryName}.\n\nPlease take a screenshot of this message, join the SMATRS Discord, and request assistance."],
        "smbxVersion": ["SMBX Versioning Error!","Could not find the engine version number.\n\nAre you sure everything is in the right place?"],
        # "": ["Error finding SMATRS Updater version from cloud!","An error occured when attempting to pull SMATRS Updater version from cloud. Are you connected to the internet?"]
    }

    messagebox.showerror(errorDict[issue][0], errorDict[issue][1])
    sys.exit(error)

def cloudIsNewer(key):
    
    print(f"Local version of {key} is", formatVersion(LOCAL[key]))
    print(f"Cloud version of {key} is", formatVersion(CLOUD[key]),"\n")

    if versionIsNewer(CLOUD[key], LOCAL[key]):
        print(f"{key} on cloud is newer")
        return True
    elif versionIsNewer(LOCAL[key], CLOUD[key]):
        
        sillyTitle = [
            "Everyone's versions got all jumbled up!",
            "THESE VERSIONS ARE REALLY ON FIRE!",
            "JUST A SIMPLE NUMBERS GAME.",
            "YOUR VERSION'S TOO HIGH! YOUR CHOICE HAS RUN OUT!",
            "THIS VERSION CANNOT BE KILLED!"
        ]

        messagebox.showinfo(random.choice(sillyTitle),f"WHO KEEPS SPINNING THE WORLD AROUND?!\n\nSomehow, your local version is HIGHER than the cloud version. Either you're a developer (hi f riend!), you've messed with something you shouldn't have (stop that!), or something has gone horrifically wrong.\n\nIf you don't know why this error might've occured, please take a screenshot of this message, join the SMATRS Discord, and send this in the #bug-report channel.\n\nTraceback: {key}")
    elif LOCAL[key] == CLOUD[key]:
        print(f"{key} is up-to-date")
    else:
        print(f"{key} query returned no results")

    return False


def tryLoadCloudJSON():
    global LOCAL, CLOUD

    for i in range(5):
        try:
            cloudJSON = urllib.request.urlopen(versionURL).read()
            cloudJSON = json.loads(cloudJSON)

            LOCAL = {
                "smbx-version": "",
                "smatrs-updater-version": [1,0,0],
                "self-updater-version": [1,0,0],
                "main-version": [1,0,0]
            }
            CLOUD = {
                "smbx-version": cloudJSON["smbx-version"][-1],
                "smatrs-updater-version": cloudJSON["smatrs-updater-version"][-1][0],
                "self-updater-version": cloudJSON["self-updater-version"][-1][0],
                "main-version": cloudJSON["main-version"]
            }

            LOCAL["smbx-version"] = tryLoadSMBXVersion()

            print(f"local:", LOCAL)
            print(f"cloud:", CLOUD)

            return
        except urllib.error.URLError as e:
            print(f"cloudJSON pull attempt {i} failed")
            print(e)
            time.sleep(3 + i**2)

    throwError("urlError", error="Failed all attempts at pulling versions from cloud")

def tryLoadSMBXVersion():
    with open(f"{os.getcwd()}/data/config/game.ini", "r") as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith("game-title"):
                continue

            for text in line.split():
                if text[0] == "(" and text[-1] == ")":
                    return text

    throwError("smbxVersion")

# Specifically for trying to pull a resource included *within* the onefile.exe
def resourcePath(relative_path):
    base_path = globals().get('bootstrapDirectory', os.path.abspath("."))

    # for context, https://nuitka.net/user-documentation/common-issue-solutions.html#onefile-finding-files
    return os.path.join(base_path, relative_path)


# This is mandatory to properly initialize LOCAL and CLOUD
# Sorry, DoubleA!
tryLoadCloudJSON()

loadedModules["universals"] = {
    'validLauncherNames': validLauncherNames,
    'validSaveFilenames': validSaveFilenames,
    'versionURL': versionURL,
    'filesURL': filesURL,
    'updateZipFilename': updateZipFilename,

    'CLOUD': CLOUD,
    'LOCAL': LOCAL,

    'everythingUpdated': everythingUpdated,

    'versionIsNewer': versionIsNewer,
    'formatVersion': formatVersion,
    'throwError': throwError,
    'cloudIsNewer': cloudIsNewer,
    'tryLoadCloudJSON': tryLoadCloudJSON,
    'tryLoadSMBXVersion': tryLoadSMBXVersion,
    'resourcePath': resourcePath,
}

