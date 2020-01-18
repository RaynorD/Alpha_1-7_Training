import os
import sys
import shutil
import platform
import subprocess
import winreg
from pathlib import Path
import cScripts

def main():
    print("""
  #######################################
  # A/1-7 Development Environment Setup #
  #######################################

  This script will create your dev environment for you.
  After running this, you can run build.py to quickly update your development PBOs.

  Before you run this, you should already have:
    - The Arma 3 Tools installed properly via Steam

  If you have not done those things yet, please abort this script now and do so first.

  This script will create the required hard links on your system:
    - (profile)/missions/A-1-7 ==> (repo)/missions
    - files and sqms within the various missions folders
  """)
    print("\n")

    scriptpath = Path(os.path.realpath(__file__))

    projectpath = scriptpath.parent.parent
    print("Project Path: {}".format(projectpath))
    

    cScripts.copy()
    
    return 0

if __name__ == "__main__":
    exitcode = main()
    if exitcode > 0:
        print("\nSetup aborted, something went wrong.")
    elif exitcode == -2:
        print("\n# Good so far")
    else:
        print("\nSetup successfully completed.")
    
    os.system("pause")

# make mission dir junction
# make files/sqm > missions dir junction
