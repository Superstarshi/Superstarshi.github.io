import os
import json
import shutil

import tkinter as tk
from tkinter import ttk, messagebox

import urllib.request
import webbrowser
import gdown

import threading
from zipfile import ZipFile

import send2trash

import random

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(2)



class SmatrsUpdater:
    def __init__(self):

        self.directory = os.getcwd()

        # Updater stuff
        self.episodePath = None
        self.version = None
        self.versionName = None

        self.saves = None


        # Application stuff
        # self.attemptUpdate()
        
        pass

    def attemptUpdate(self):
        try:
            self.findEpisode(deleteRedundant=True)

            self.gameUpdate()
        except Exception as e:
            print("SMATRS Updater found issue while updating:\n" + str(e))
            # os.abort()

    
    def getVersionFromInfoFile(self,path):
        # In a decent language, this would look nice
        # Open the info.json file
        filePath = f"{path}\\launcher\\info.json"

        try:
            file = open(filePath,"r")
        except:
            file.close()
            return
        
        # Read its contents
        rawContents = None
        
        try:
            rawContents = file.read()
        except:
            getModule("universals")["throwError"]("parsingError",f"Failed to read info.json at {filePath}")
            file.close()
            return
        
        # Parse it
        parsedContents = None

        try:
            parsedContents = json.loads(rawContents)
        except:
            getModule("universals")["throwError"]("parsingError",f"Failed to parse info.json at {filePath}")
            file.close()
            return
        
        # Does it contain a version?
        if not "current-version" in parsedContents:
            getModule("universals")["throwError"]("parsingError",f"info.json at {filePath} lacks a version number")
            file.close()
            return

        file.close()
        return parsedContents["current-version"]



    def findSaveFiles(self,folderPath):
        saveFiles = []

        for save in os.scandir(folderPath):
            if not save.is_file():
                continue
            
            # f is intentionally not f.lower() here; in case there is ever another file created (eg. "somethingProgress.json"), camelcase should exclude it
            # ^ windows isn't case sensitive about filenames
            for f in getModule("universals")["validSaveFilenames"]:
                if f.lower() in save.name:
                    saveFiles.append(save.path)
                    break

        print(f"\nSearched for saves in path {folderPath} and found {len(saveFiles)} file(s):")
        for s in saveFiles:
            print(f'    ...\\{os.path.basename(s)}')
        return saveFiles
    
    def moveFiles(self,filepathsToMove,directoryMoveTo):
        if not isinstance(filepathsToMove,list):
            filepathsToMove = [filepathsToMove]

        finishedPaths = []

        # Move shit out the way if we've already failed mid-update before
        if os.path.exists(directoryMoveTo):
            backup = f"{directoryMoveTo}-backup"
            if os.path.exists(backup):
                send2trash.send2trash(backup)
            os.rename(directoryMoveTo,backup)

        if not os.path.exists(directoryMoveTo):
            os.makedirs(directoryMoveTo)

        for f in filepathsToMove:
            try:
                filename = os.path.basename(f)
                os.rename(src=f,dst=f'{directoryMoveTo}\\{filename}')
                finishedPaths.append(f'{directoryMoveTo}\\{filename}')
            except Exception as e:
                print(e)
                getModule("universals")["throwError"]("filenameError",f)
        
        print(f"\nMoved {len(finishedPaths)} file(s) to {directoryMoveTo}:")
        for f in finishedPaths:
            print(f'    ...\\{os.path.basename(f)}')

        return finishedPaths



    def getEpisodeFolders(self,launcherPath):
        worldsPath = f"{launcherPath}\\data\\worlds\\"
        episodes = []

        for worldFolder in os.scandir(worldsPath):
            if not worldFolder.is_dir():
                continue

            if not worldFolder.name.lower().startswith("smatrs"):
                continue

            episodes.append({
                "path": worldFolder.path,
                "version": self.getVersionFromInfoFile(worldFolder.path),
            })
        
        return episodes

    def findEpisode(self,deleteRedundant=False):
        foundEXE = False
        for filename in os.listdir(self.directory):
            if not filename.lower() in getModule("universals")["validLauncherNames"]:
                continue

            print("Found valid launcher as",filename)
            foundEXE = True

            candidateEpisodes = self.getEpisodeFolders(self.directory)

            for episode in candidateEpisodes:
                if self.version == None or getModule("universals")["versionIsNewer"](episode["version"], self.version):
                    self.episodePath = episode["path"]
                    self.version = episode["version"]
        
        if not foundEXE:
            getModule("universals")["throwError"]("noEXE")
        elif self.episodePath == None:
            # getModule("universals")["throwError"]("smatrsnotfound")
            self.gameInstall()
            return
        
        self.versionName = getModule("universals")["formatVersion"](self.version)

        print(f"Found install ({self.versionName}) at {self.episodePath}")

        if deleteRedundant and len(candidateEpisodes) > 1:
            okToDelete = messagebox.askyesno("Multiple SMATRS folders found!",f"Multiple instances of the SMATRS folder have been found in the data\\worlds\\ directory.\n\nMost recent version has been identified as {self.versionName} in directory\n{self.episodePath}\n\nMove redundant copies to Recycle Bin?")

            if okToDelete:
                deletedDirectories = ""
                print(f"\nDeleted folders in {self.directory}\\data\\worlds:")

                for episode in candidateEpisodes:
                    epiPath = episode["path"]
                    if epiPath == self.episodePath:
                        continue

                    send2trash.send2trash(epiPath)
                    print(f'    ...' + epiPath[epiPath.rfind("\\"):] + '\\')
                    deletedDirectories += f'{epiPath}\n'
                
                messagebox.showinfo("Redundant Folders Successfully Removed",f"Cleanup success! The following directories have been removed:\n\n{deletedDirectories}")



    def gameUpdate(self):
        cloudVersion = self.findURLData("current-version")

        # If the version on cloud is newer than the version on local,
        if getModule("universals")["versionIsNewer"](cloudVersion,self.version):
            doUpdate = messagebox.askyesno("Local Version Outdated!",f'Local install of SMATRS {self.versionName} is outdated; latest is {getModule("universals")["formatVersion"](cloudVersion)}. Do you want to install the latest version? (Your save files will be safe!)')

            # and if an update is desired, run updates
            if not doUpdate:
                return False
        # If the version on local is, somehow, newer than the version on cloud, do funny
        elif getModule("universals")["versionIsNewer"](self.version,cloudVersion):
            sillyTitle = [
                "Everyone's versions got all jumbled up!",
                "THESE VERSIONS ARE REALLY ON FIRE!",
                "JUST A SIMPLE NUMBERS GAME.",
                "YOUR VERSION'S TOO HIGH! YOUR CHOICE HAS RUN OUT!"
            ]

            messagebox.showinfo(random.choice(sillyTitle),f"WHO KEEPS SPINNING THE WORLD AROUND?!\n\nSomehow, your local SMATRS version is HIGHER than the cloud version. Either you're a developer (hi f riend!), you've messed with something you shouldn't have (stop that!), or something has gone horrifically wrong.")
            return
        # If neither are greater than each other, then they're equal. Local is up-to-date with cloud
        else:
            messagebox.showinfo("You're enthusiastic!",f'Local install {self.versionName} is up-to-date :)')
            return

        # Find saves
        self.saves = self.findSaveFiles(self.episodePath)

        # Find the URL to download from
        episodeURL = self.findURLData("google-drive-url")
        
        # Download the zip from google drive
        updateFile = self.getZip(episodeURL)

        # Move the save files from the outdated directory to a temporary safekeeping directory
        self.saves = self.moveFiles(self.saves,tempDirectoryPath)

        # Trash the outdated directory
        send2trash.send2trash(self.episodePath)

        # Unzip the new version and place it in the data\worlds\ folder
        try:
            with ZipFile(updateFile,"r") as file:
                file.extractall(f"{self.directory}\\data\\worlds")
                file.close()
        except Exception as e:
            print(str(e))
            getModule("universals")["throwError"]("unzipError",updateFile)

        # Find the new version, since it may be different from the old version
        self.findEpisode()

        # Move the saves into the new folder
        self.saves = self.moveFiles(self.saves,self.episodePath)

        # Delete the temporary directory and downloaded zip
        shutil.rmtree(tempDirectoryPath)
        try:
            os.remove(updateFile)
        except Exception as e:
            try:
                send2trash.send2trash()
            except Exception as ex:
                print(f"Failed to remove zip. Error log:\n\n{e}\n\n{ex}")

        # Done, I think...?
        messagebox.showinfo("Success!",f"SMATRS {self.versionName} has been successfully downloaded. You may want to empty your recycle bin.")

    def gameInstall(self):
        doInstall = messagebox.askyesno("SMATRS not found!",f'The data\\worlds\\ directory does not contain any folders titled "SMATRS". Do you want to install the game?')

        if not doInstall:
            return

        # Find the URL to download from
        episodeURL = self.findURLData("google-drive-url")
        
        # Download the zip from google drive
        updateFile = self.getZip(episodeURL)

        # Unzip the new version and place it in the data\worlds\ folder
        try:
            with ZipFile(updateFile,"r") as file:
                file.extractall(f"{self.directory}\\data\\worlds")
                file.close()
        except:
            getModule("universals")["throwError"]("unzipError",updateFile)

        # Find the install
        self.findEpisode()

        # Delete the downloaded zip
        try:
            os.remove(updateFile)
        except Exception as ex:
            print(f"Failed to remove zip. Error log:\n{ex}")

        # Done
        messagebox.showinfo("Success!",f"SMATRS {self.versionName} has been successfully downloaded. Have fun playing!")



    def findURLData(self,key):
        try:
            smatrsSite = urllib.request.urlopen(getModule("universals")["versionURL"])
        except:
            getModule("universals")["throwError"]("connectionError")
            return
        

        cloudJSON = smatrsSite.read()

        # thanks doublea :3

        try:
            cloudJSON = json.loads(cloudJSON)
        except:
            getModule("universals")["throwError"]("urlError","Failed to parse JSON from cloud")
            return
        
        # Does it contain the key?
        if not key in cloudJSON:
            getModule("universals")["throwError"]("urlError",f'JSON from cloud lacks key "{key}"')
            return

        return cloudJSON[key]

    def getZip(self,downloadURL,tries=3):
        # create variable for later
        update_file = None

        print(f"\nAttempting install from URL {downloadURL}\n")

        for t in range(tries):
            try:
                print(f"    Attempt {t+1}/{tries}")
                update_file = gdown.download(url=downloadURL,output=f"{self.directory}\\{getModule("universals")["updateZipFilename"]}")
                print(f"\n        Attempt {t+1}/{tries} success")
                
                return update_file
            except Exception as err:
                print(f"        Attempt {t+1}/{tries} failed; ", err)
                continue

        getModule("universals")["throwError"]("downloadFail")

loadedModules["smatrsUpdater"] = {
    'SmatrsUpdater': SmatrsUpdater
}


#
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣀⣀⠀⠀⣀⡠⠴⠒⠚⠉⠉⠓⠒⠦⣄⣶⠒⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡷⢬⣉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠠⡌⠻⣧⢻⣧⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣖⠗⡋⢹⠀⠀⢰⡄⠀⠀⢸⣷⡀⠀⣠⠽⣆⢼⣇⢻⣸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⣡⣶⢋⡏⠙⢢⣏⣇⠀⠀⠈⣇⡵⡏⠀⠀⢹⡏⢾⣿⠃⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⢿⢻⣏⣿⡇⡄⣾⠀⠹⡄⠄⠀⡇⠀⠹⣤⠈⠹⣿⣾⢸⠀⢘⣷⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣯⣿⣽⣿⣷⢸⡗⠦⣄⡹⣼⣄⣿⣴⠛⠹⡄⡇⣿⣿⠾⠚⢹⢿⢽⣽⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣞⣾⣿⢿⣯⢻⢻⡴⠞⠁⠈⠻⣿⣌⡉⠓⣿⣰⡿⠀⠀⠀⠸⡜⡾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⣡⠊⢸⣹⠁⠈⠙⣾⡄⠁⠀⢰⠛⠉⠉⠉⢳⣀⣿⣿⠃⠀⠀⣀⣀⣧⣿⡞⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⡴⠁⠀⠸⢿⣤⣤⣤⣹⣿⣷⣶⣾⣷⣶⣶⣺⣋⣽⣿⣷⠶⠟⠛⠋⢧⠀⠀⠸⡜⣷⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⠁⡰⠁⠀⠀⢠⡿⠀⠀⠀⠉⠉⠉⠙⢻⡟⣹⣿⠃⣿⠋⠁⠀⠀⠀⠀⠀⠸⡄⠀⠀⢣⠹⣧⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⡀⢠⠇⠀⠀⢠⡿⠁⠀⠀⠀⠀⣤⣶⡴⠚⢻⠡⣸⠀⢹⣆⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠸⡄⢻⣇⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⣼⠁⢸⠀⠀⠀⣾⠃⠀⠀⠀⠀⠀⢻⣿⣧⣀⣬⠋⠁⠀⣠⣿⣶⣆⠀⠀⠀⠀⠀⡇⠀⠀⠀⡇⠈⣿⡀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣸⣿⠀⡇⠀⢰⣸⡟⠀⠀⠀⣀⣠⠴⠚⣟⣻⣧⣯⣗⣤⣾⣿⣿⡿⠋⠀⠀⠀⠀⣸⣤⠀⠀⠀⡇⡆⢻⠃⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⢸⡀⣇⠀⣸⣿⡁⠀⣾⣻⡁⣀⣤⣶⠟⠋⠉⠛⢿⣋⣻⡏⠉⠀⠀⠀⠀⠀⢰⣿⡇⠀⠀⠀⣷⡇⣸⡄⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠇⠀⢧⢸⠀⣿⡿⠇⠀⠈⠛⠛⠋⠉⠀⠀⠀⠀⠀⡟⠀⣿⠇⠀⠀⠀⠀⠀⢠⣿⣿⡇⠀⠀⣰⡿⣧⣿⠃⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣄⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⣿⠀⠀⠀⠀⠀⠀⣸⡿⢸⠁⢠⣾⠋⢰⣿⡏⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣶⣶⡿⠀⠀⠀⠀⠀⠀⠉⠁⢸⣶⡟⠁⠀⠾⠟⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀