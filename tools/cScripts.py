import os
import subprocess
from pathlib import Path
import fnmatch
import shutil

scriptpath = Path(os.path.realpath(__file__))
projectpath = scriptpath.parent.parent
cscriptspath = os.path.join(projectpath,'cScripts')

def pull():

    print("")

    # Checkout latest cScripts release
    print("  ===== Checking out latest cScripts release")

    os.chdir(cscriptspath)
    subprocess.check_output(["git", "config", "--global", "advice.detachedHead","false"])
    commit_id = subprocess.check_output(["git", "rev-list", "--tags", "--max-count=1"])
    commit_id = str(commit_id, "utf-8")[:8]
    tag_text = subprocess.check_output(["git", "describe", "--tags", commit_id])
    tag_text = str(tag_text, "utf-8")[:8]

    subprocess.check_output(["git", "checkout", commit_id])

    print("  ===== Pulled cScripts latest release: {}".format(tag_text))

def copy():
    print("  ===== Copying cScripts into files")
    
    filespath = os.path.join(projectpath,"files")
    
    # copy cScripts folder
    if(os.path.isdir(os.path.join(filespath,"cScripts"))):
        shutil.rmtree(os.path.join(filespath,"cScripts"))

    shutil.copytree(os.path.join(cscriptspath,"cScripts"),os.path.join(filespath,"cScripts"))
    
    # copy files
    shutil.copy(os.path.join(cscriptspath,"cba_settings.sqf"),os.path.join(filespath,"cba_settings.sqf"))
    shutil.copy(os.path.join(cscriptspath,"initServer.sqf"),os.path.join(filespath,"initServer.sqf"))
    
    print("  ===== cScripts updated. Reminder: init.sqf and description.ext were not replaced.")

if __name__ == '__main__':
    #pull()
    copy()
