import os
import glob
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory
from enum import IntEnum, auto

# constants

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

def getSlot():
    '''
    This queries the user for the slot to delete.
    :returns:
        - slot - the slot number to delete from
    '''
    f = input("Delete from which slot? ")
    f = int(f)
    return f

def mainLoop():
    again = True
    same = False
    
    while again:

        op = queryOperation()

        if op is Operation.QUIT:
            return
        
        if not same:
            modFolder = getModFolder()
 
        doOperation(modFolder, op)
        
        again = queryYN("Again?")
        same = queryYN("Same root folder?")


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
                
        print(bcolors.FAIL + "Please select one of the presented options." + bcolors.ENDC)

def getModFolder():
    '''
    This queries the user for the mod folder root.
    :returns:
        - modFolder - the user's chosen directory
    '''
    
    print("select the mod folder")
    Tk().withdraw()
    modFolder = askdirectory(title="Select the root mod folder")
    return modFolder

def doOperation(modFolder, op):
    if op is Operation.COPY or op is Operation.REPLACE:
        doCopyReplace(modFolder, op)
    else:
        doDelete(modFolder)

def queryYN(query):    
    yesNo = {"yes": True, "no": False, "yeah": True, "yeet": True, "nahhhhhhh": False, "sure": True}
    while True:
        choice = input(query + " (y/n) ").lower().strip()

        for answer, bool in yesNo.items():
            if choice in answer:
                return bool
            
        print(bcolors.FAIL + "Please answer yes or no." + bcolors.ENDC)

def doCopyReplace(modFolder, op):
    ok = False
    while not ok:
        fromSlot, toSlot = getSlots()
        ok, msg = validateRequest(fromSlot, toSlot, modFolder)
        if not ok:
            print(bcolors.FAIL + msg + bcolors.ENDC)
            input()

    cPath = msg
    
    print(bcolors.OKGREEN + "{} character mods from {} to slot {}".format(operations[op], cPath, toSlot)  + bcolors.ENDC)

    if op is Operation.COPY:
        modFolder = copyFolder(modFolder, toSlot)
    files = getFilesToChange(fromSlot, modFolder)
    
    changeFiles(modFolder, files, fromSlot, toSlot)

def getSlots():
    '''
    This queries the user for slots to copy/move from and to.
    :returns:
        - from - the slot number to copy/move from
        - to - the slot number to copy/move to
    '''
    f = input("Move from which slot? ")
    t = input("Move to which slot? ")
    f = int(f)
    t = int(t)
    return f,t
   
def validateRequest(fromSlot, toSlot, modFolder):
    '''
    This validates copy/move requests.

    :param int fromSlot: the slot to move/copy a mod from
    :param int toSlot: the slot to move/copy a mod to
    :param string modFolder: the root path of the mod folder 
    :returns:
        - bool - whether the validation was successful
        - msg - if successful, the c0X directory of the slot to copy/move from
                if unsuccessful, the reason for failure
    '''
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

def copyFolder(folder, toSlot):
    newFolder = "{}.0{}".format(folder,toSlot)
    files = os.listdir(folder)
    shutil.copytree(folder,newFolder)
    return newFolder


def getFilesToChange(slot, folder):
    '''
    This gets the list of files which should be operated upon.
    :param int fromSlot: the slot to delete a mod from
    :param string modFolder: the root path of the mod folder 
    :returns:
        - modFolder - the user's chosen directory
    '''
    filePattern = r"**\*0{}.*".format(slot)
    folderPattern = r"**\c0{}\\".format(slot)
    files = glob.glob(folderPattern, root_dir=folder, recursive=True)
    folders = glob.glob(filePattern, root_dir=folder, recursive=True)
    return files + folders # return files and folders :)

def changeFiles(folder, files, fromSlot, toSlot):
    sFrom = "0{}".format(fromSlot)
    sTo = "0{}".format(toSlot)
    for file in files:
        oldFile = "{}\\{}".format(folder,file)
        newFile = "{}\\{}".format(folder,file.replace(sFrom, sTo))
        os.rename(oldFile, newFile)




mainLoop()



