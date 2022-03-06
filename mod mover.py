import os
import glob
from tkinter import Tk
from tkinter.filedialog import askdirectory
from enum import Enum, auto


class Operation(Enum):
    COPY = 1
    REPLACE = auto()
    FINAL = auto()

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

    op = queryOperation():

    operations = {Operation.COPY: "copying", Operation.REPLACE: "moving"}
    print("{} character mods from {} to slot {}".format(operations[op], cPath, toSlot))
    files = getFilesToChange(fromSlot, modFolder)

def queryOperation():
    prompt = """Copy to new mod folder or replace existing files?
    \t1. Copy
    \t2. Replace
    \n"""

    options = {Operation.COPY: "copy", Operation.REPLACE: "replace",}

    
    while True:
        sys.stdout.write(prompt)
        choice = input().lower()

        if choice.isdigit() and 0 < int(choice) and int(choice) < Operation.FINAL:
            return Operation(int(choice))
        elif choice in options[Operation.COPY]:
            return Operation.COPY
        elif choice in options[Operation.REPLACE]:
            return Operation.REPLACE
        else:
            sys.stdout.write("Please select one of the presented options.\n")

mainLoop()



