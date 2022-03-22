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
    """
    This validates copy/move requests.

    :param int fromSlot: the slot to move/copy a mod from
    :param int toSlot: the slot to move/copy a mod to
    :param string modFolder: the root path of the mod folder 
    :returns:
        - bool - whether the validation was successful
        - msg - if successful, the c0X directory of the slot to copy/move from
                if unsuccessful, the reason for failure
    """
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
    fromcDir = cDirs[0]
    tocDir = fromcDir[:-2]+"{}".format(toSlot)+"\\"
    
    # if folder path doesn't end with \, add it
    if modFolder[-1] != "\\": modFolder = modFolder + "\\"
    
    toPath = modFolder + tocDir
    if os.path.isdir(toPath):
        return False, "{} already exists".format(toPath)

    return True, "{}{}".format(modFolder,fromcDir)

def getModFolder():
    """
    This queries the user for the mod folder root.
    :returns:
        - modFolder - the user's chosen directory
    """
    
    print("select the mod folder")
    Tk().withdraw()
    modFolder = askdirectory(title="Select the root mod folder")
    return modFolder

def getSlots():
    """
    This queries the user for slots to copy/move from and to.
    :returns:
        - from - the slot number to copy/move from
        - to - the slot number to copy/move to
    """
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
    again = True 
    
    while again:
        modFolder = getModFolder()
        fromSlot, toSlot = getSlots()
        ok, msg = validateRequest(fromSlot, toSlot, modFolder)
        if not ok:
            print(msg)
            input()
        cPath = msg
    
        op = queryOperation()
    
        print("{} character mods from {} to slot {}".format(operations[op], cPath, toSlot))
    
        if op is Operation.QUIT:
            return
        elif op is Operation.COPY:
            modFolder = copyFolder(modFolder, toSlot)
        files = getFilesToChange(fromSlot, modFolder)
    
        changeFiles(modFolder, files, fromSlot, toSlot)
        
        again = queryYN() 

def queryYN():    
    yesNo = {"yes": True, "no": False, "yeah": True, "yeet": True, "nahhhhhhh": False, "sure": True}
    while True:
        choice = input("Again? (y/n) ").lower().strip()

        for answer, bool in yesNo.items():
            if choice in answer:
                return bool
                
        print("Please answer yes or no.")

def queryOperation():
    prompt = "Copy to new mod folder or replace existing files?\n"

    for enum, operation in operations.items():
        prompt += "\t{}. {}\n".format(int(enum), operation.title())
    
    while True:
        choice = input(prompt).lower()

        if choice.isdigit():
            iChoice = int(choice)
            if 0 < iChoice and iChoice < Operation.FINAL:
                return Operation(int(choice))
        else:
            for enum, operation in operations.items():
                if choice in operation:
                    return enum
                
        print("Please select one of the presented options.")

mainLoop()



