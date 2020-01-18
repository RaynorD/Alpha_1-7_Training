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
    print("===== Checking out latest cScripts release")

    os.chdir(cscriptspath)
    subprocess.check_output(["git", "config", "--global", "advice.detachedHead","false"])
    commit_id = subprocess.check_output(["git", "rev-list", "--tags", "--max-count=1"])
    commit_id = str(commit_id, "utf-8")[:8]
    tag_text = subprocess.check_output(["git", "describe", "--tags", commit_id])
    tag_text = str(tag_text, "utf-8")[:8]

    subprocess.check_output(["git", "checkout", commit_id])

    print("===== Pulled cScripts latest release: {}".format(tag_text))
    
    print("")
    print("")

def copy():
    print("Deleting old cScripts")
    
    os.chdir(os.path.join(projectpath,"files"))
    
    # Remove cScripts folder
    shutil.rmtree(os.path.join(projectpath,"files","cScripts"))
    
    # Remove cScripts-X.X.X.md
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'cScripts-*'):
            
            os.remove(file)

if __name__ == '__main__':
    #pull()
    copy()
