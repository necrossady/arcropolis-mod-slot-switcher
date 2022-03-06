import os
import glob
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askdirectory

def validateRequest(fromSlot, toSlot, modFolder):
    # ensure slots are 0-7
    if not(isinstance(fromSlot,int) and isinstance(toSlot,int)):        
        return False, "slots must be integers"
    elif (
        fromSlot < 0 or toSlot < 0 or
        fromSlot > 7 or toSlot > 7
        ):
        return False, "slots must be 0-7"
            
    # ensure modFolder exists
    # ??? this will fail for UI-only mods, will need to address that if it should work with them
    cglob = "**\\[cC]0{}\\".format(fromSlot)
    cDirs = glob.glob(cglob, root_dir=modFolder, recursive=True)
    
    if len(cDirs) < 1:
        return False, "no c0{} found in {}".format(fromSlot, modFolder)

    # NEEDS HANDLING FOR MULTI MODELS
    
    # ensure modFolder does not already have a mod in slot to
    fcDir = cDirs[0]
    tcDir = fcDir[:-2]+"{}".format(toSlot)+"\\"
    
    if modFolder[-1] != "\\": modFolder = modFolder + "\\"
    
    toPath = modFolder + tcDir
    if os.path.isdir(toPath):
        return False, "{} already exists".format(toPath)

    return True, "{}{}".format(modFolder,fcDir)

def getModFolder():
    print("select the mod folder")
    Tk().withdraw()
    modFolder = askdirectory(title="Select the root mod folder")
    return modFolder

def getSlots():
    f = input("Move from which slot? ")
    t = input("Move to which slot? ")
    f = int(f)
    t = int(t)
    return f,t

def getFilesToChange(fromSlot, folder):
    filePattern = r"**\*0{}.*".format(fromSlot)
    return glob.glob(filePattern, root_dir=folder, recursive=True)

def mainLoop():
    modFolder = getModFolder()
    fromSlot, toSlot = getSlots()
    ok, cPath = validateRequest(fromSlot, toSlot, modFolder)
    if not ok:
        print(msg)
        input()
        return

    print("Valid input...")
    print("Valid input, moving character mods from {} to slot {}".format(cPath, toSlot))
    files = getFilesToChange(fromSlot, modFolder)

mainLoop()



