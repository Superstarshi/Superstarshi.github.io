import urllib.request
import time

def updateFile(filename):
    print(f"Attempting to update {filename}\n")
    verOnCloud = ""
    for i in range(3):
        try:
            verOnCloud = urllib.request.urlopen(getModule("universals")["filesURL"] + f"/{filename}.py").read()
        except Exception as e:
            print(f"Cloud file pull attempt {i} failed;\n{e}")
            time.sleep(3 + i**2)

    if verOnCloud == "":
        getModule("universals")["throwError"]("urlError", error="Failed all attempts at pulling versions from cloud")

    with open(updaterDirectoryName + f"\\{filename}.py", "w") as file:
        file.write(verOnCloud)

loadedModules["selfUpdater"] = {
    'updateFile': updateFile,
}
