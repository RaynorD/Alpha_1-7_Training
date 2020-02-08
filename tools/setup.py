import os
import sys
import shutil
import platform
import subprocess
import winreg
import pathlib
import ctypes.wintypes
import fnmatch
import tempfile
import time
from urllib.parse import unquote

missionName = "Alpha_1-7_Training"

scriptpath = pathlib.Path(os.path.realpath(__file__))

projectpath = scriptpath.parent.parent

sqmfolder = os.path.join(projectpath,"sqm")
missionsfolder = os.path.join(projectpath,"missions")
filespath = os.path.join(projectpath,"files")

A17Folder = ""

def main():
    print("""
  #######################################
  # A/1-7 Development Environment Setup #
  #######################################

  This script will build the dev environment for the 7th Cavalry A/1-7 training missions.
  
  It will setup the required links on your system:
    - Junction for (profile)/missions/A-1-7 ==> (repo)/missions
    - Mission directories in repo/missions
  
  After running this, you can then open and edit the missions in the Arma editor,
    in the new A-1-7 folder.
  
  NOTE: The "Export to Multiplayer" option in the editor does not understand
    symlinks and will not work with this setup.
    
  In order to export all PBOs for MP testing and release, run build.py.
  """)
  
    #try:
    #    con = input('Continue? (y/n) : ')
    #except SyntaxError:
    #    con = None
    #
    #if(con != 'y' or con is None):
    #    return -1
    
    print("\n")
    
    print("  Project Path: {}".format(projectpath))
    
    code = make_folders()
    if(code != 0):
        return code
    
    code = make_links()
    if(code != 0):
        return code
    
    return 0

def clear_folder(folder):
    parentFolder = os.path.dirname(folder)
    os.chdir(parentFolder)
    if(os.path.isdir(folder)):
        print("  Removing folder {}".format(folder))
        dirs = os.listdir(".")
        for dir in dirs:
            if(os.path.isdir(os.path.join(folder,dir))):
                shutil.rmtree(dir)
        time.sleep(0.5)
        print("    parentFolder = {}".format(parentFolder))
        tmp = tempfile.mkdtemp(dir=parentFolder)
        time.sleep(0.5)
        print("    tmp = {}".format(tmp))
        shutil.move(folder, tmp)
        time.sleep(0.5)
        shutil.rmtree(tmp)
        time.sleep(0.5)
    os.mkdir(os.path.basename(os.path.normpath(folder)))
    return

def make_folders():
    # =========== Create Repo/missions
    os.chdir(projectpath)
    
    clear_folder(missionsfolder)
    
    
    # =========== Create Missions/A-1-7
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    armaprofilesfolder = os.path.join(buf.value,"Arma 3 - Other Profiles")

    #print("  Profiles folder: {}".format(armaprofilesfolder))
    
    dirs = os.listdir(path=armaprofilesfolder)
    
    if(len(dirs) > 1):
        print("  Multiple Arma 3 profiles found - please select a profile:")
        print("    0 - Exit")
        for num, profile in enumerate(dirs, start=1):
            print("    {} - {}".format(num,unquote(profile)))

        cont = False
        
        while(cont is False):
            try:
                sel = int(input('Please select a profile: '))
                if(sel >= 0 and sel <= len(dirs)):
                    cont = True
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input, please enter a number between 0 and {}".format(len(dirs)))
        
        if(sel == 0):
            return -1
        
        profileName = dirs[sel-1]
    elif (len(dirs) == 0):
        print("Error: No profiles found")
        return 1
    else:
        profileName = dirs[0]
    
    #print("  Using profile: {}".format(profileName))
    profileMissionsFolder = os.path.join(armaprofilesfolder,profileName,"missions")
    print("  Using missions folder: {}".format(profileMissionsFolder))
    
    global A17Folder
    A17Folder = os.path.join(profileMissionsFolder,"A-1-7")
    clear_folder(A17Folder)
    
    os.chdir(profileMissionsFolder)
    time.sleep(0.25)
    
    os.mkdir("A-1-7")
    return 0

def make_links():
    # ========= Populate missions folder
    os.chdir(sqmfolder)
    maps = []
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.sqm'):
            maps.append(file)
    
    
    for sqm in maps:
        mapname = sqm.replace(".sqm","")
        missionFolderName = "{}.{}".format(missionName,mapname)
        missionFolder = os.path.join(missionsfolder,missionFolderName)
        os.chdir(missionsfolder)
        os.mkdir(missionFolderName)
        time.sleep(0.05)
        
        # Link SQM
        try:
            #print("Linking SQM".format(os.path.join(missionFolder,"mission.sqm"), os.path.join(sqmfolder,sqm)))
            subprocess.call(["cmd", "/c", "mklink", str(os.path.join(missionFolder,"mission.sqm")), str(os.path.join(sqmfolder,sqm))])
        except:
            return 1
            print("  ERROR: Could not create SQM link")
        time.sleep(0.1)
        
        # Create junctions in A-1-7
        global A17Folder
        A17MissionFolder = os.path.join(A17Folder,missionFolderName)
        try:
            #print("Trying to link folder \n{} ==> \n{}".format(A17MissionFolder,missionFolder))
            subprocess.call(["cmd", "/c", "mklink", "/D", str(os.path.join(A17MissionFolder)), str(os.path.join(missionFolder))])
        except:
            return 1
            print("  ERROR: Could not create SQM link")
        time.sleep(0.1)
        
        create_all_links(missionFolder,filespath)
    
    return 0

def create_all_links(link,target):
    #(missionFolder,filespath)
    dirCount = 0
    fileCount = 0
    for thing in os.listdir(target):
        if(not os.path.isdir(os.path.join(target,thing))):
            # Link File
            try:
                #print("Linking file: {} ==> {}".format(os.path.join(link,thing), os.path.join(target,thing)))
                subprocess.call(["cmd", "/c", "mklink", str(os.path.join(link,thing)), str(os.path.join(target,thing))])
            except:
                print("  ERROR: Could not create symbolic link")
            fileCount += 1
            print("\n")
            time.sleep(0.05)
        else:
            # Link directory
            try:
                #print("Linking directory: {} ==> {}".format(os.path.join(link,thing), os.path.join(target,thing)))
                subprocess.call(["cmd", "/c", "mklink", "/D", str(os.path.join(link,thing)), str(os.path.join(target,thing))])
            except:
                print("  ERROR: Could not create directory junction")
            dirCount += 1
            print("\n")
            time.sleep(0.25)
    print("  Linked {} top level files".format(fileCount))
    print("  Linked {} directories".format(dirCount))
    return 0

if __name__ == "__main__":
    exitcode = main()
    if exitcode > 0:
        print("\n  Setup aborted, something went wrong.")
    elif exitcode == -1:
        print("\n  Setup aborted, no changes were made.")
    else:
        print("\n  Setup successfully completed.")
    
    #os.system("pause")

# make mission dir junction
# make files/sqm > missions dir junction
