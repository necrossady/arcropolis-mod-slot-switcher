import os
import glob
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory
from enum import IntEnum, auto


class Operation(IntEnum):
    COPY = 1
    REPLACE = auto()
    QUIT = auto()
    FINAL = auto()

operations = {
    Operation.COPY: "copy",
    Operation.REPLACE: "replace",
    Operation.QUIT: "quit"
    }
   
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
    folderPattern = r"**\c0{}\\".format(fromSlot)
    files = glob.glob(folderPattern, root_dir=folder, recursive=True)
    folders = glob.glob(filePattern, root_dir=folder, recursive=True)
    return files + folders

def copyFolder(folder, toSlot):
    newFolder = "{}.0{}".format(folder,toSlot)
    files = os.listdir(folder)
    shutil.copytree(folder,newFolder)
    return newFolder

def changeFiles(folder, files, fromSlot, toSlot):
    sFrom = "0{}".format(fromSlot)
    sTo = "0{}".format(toSlot)
    for file in files:
        oldFile = "{}\\{}".format(folder,file)
        newFile = "{}\\{}".format(folder,file.replace(sFrom, sTo))
        os.rename(oldFile, newFile)

def mainLoop():
    while True:
        modFolder = getModFolder()
        fromSlot, toSlot = getSlots()
        ok, cPath = validateRequest(fromSlot, toSlot, modFolder)
        if not ok:
            print(msg)
            input()
            return
    
        op = queryOperation()
    
        print("{} character mods from {} to slot {}".format(operations[op], cPath, toSlot))
    
        if op is Operation.QUIT:
            return
        elif op is Operation.COPY:
            modFolder = copyFolder(modFolder, toSlot)
        files = getFilesToChange(fromSlot, modFolder)
    
        changeFiles(modFolder, files, fromSlot, toSlot)

def queryOperation():
    prompt = "Copy to new mod folder or replace existing files?\n"

    for enum, operation in operations.items():
        prompt += "\t{}. {}\n".format(int(enum), operation.title())
    
    while True:
        sys.stdout.write(prompt)
        choice = input().lower()

        if choice.isdigit():
            iChoice = int(choice)
            if 0 < iChoice and iChoice < Operation.FINAL:
                return Operation(int(choice))
        else:
            for enum, operation in operations.items():
                if choice in operation:
                    return enum
                
        sys.stdout.write("Please select one of the presented options.\n")

mainLoop()



