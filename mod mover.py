import os
import glob


def validateRequest(fromSlot, toSlot, modFolder):
    # ensure slots are 0-7
    if (
        not(isinstance(fromSlot,int) and isinstance(toSlot,int))
        or fromSlot < 0 or toSlot < 0
        or fromSlot > 7 or toSlot > 7
        ):
        return False, "slots must be integers 0-7"
    
    # ensure modFolder exists
    # ??? this will fail for UI-only mods, will need to address that if it should work with them
    cglob = "**\\[cC]0{}\\".format(fromSlot)
    cDirs = glob.glob(cglob, root_dir=modFolder, recursive=True)
    if len(cDirs) < 1:
        return False, "no c0{} found in {}".format(fromSlot, modFolder)
    elif len(cDirs) > 1:
        return False, "too many c0{}s found in {}! only 1 should exist".format(fromSlot, modFolder)
    
    # ensure modFolder does not already have a mod in slot to
    fcDir = cDirs[0]
    tcDir = fcDir[:-2]+"{}".format(toSlot)+"\\"
    if modFolder[-1] != "\\": modFolder = modFolder + "\\"
    toPath = modFolder + tcDir
    if os.path.isdir(toPath):
        return False, "{} already exists".format(toPath)

    return True, ""

def getFilesToChange(fromSlot, folder):
    # go through folder:
    #   get c0X folder where X is fromSlot
    #   change _0X files where X is fromSlot
    pass

