import urllib.request
import time

def updateFile(filename):
    print(f"Attempting to update {filename}\n")
    verOnCloud = None
    for i in range(3):
        try:
            verOnCloud = urllib.request.urlopen(getModule("universals")["scriptsURL"] + f"/{filename}.py").read()
        except Exception as e:
            print(f"Cloud file pull attempt {i+1}/3 failed;\n{e}")
            time.sleep(3 + i**2)

    if verOnCloud == None:
        print("Failed all cloud pull attempts")
        getModule("universals")["throwError"]("urlError", error=f"Failed all attempts at pulling {filename} data from cloud")

    verOnCloud = verOnCloud.decode()

    with open(resourcesDirectoryPath + f"\\{filename}.py", "w") as file:
        file.write(verOnCloud)

    return True

loadedModules["selfUpdater"] = {
    'updateFile': updateFile,
}
