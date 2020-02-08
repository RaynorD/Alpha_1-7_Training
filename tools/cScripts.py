import os
import subprocess
from pathlib import Path
import fnmatch
import shutil
import urllib.request
import json
import zipfile
import tempfile
import time
from setup import clear_folder

scriptpath = Path(os.path.realpath(__file__)).parent
projectpath = scriptpath.parent
cscriptspath = os.path.join(projectpath,'cScripts')

def getLatest():
    live = True
    print("  Checking latest cScripts release...")
    data = {}
    raw_json = {}
    code = 0
    if(live):
        url = 'https://api.github.com/repos/7Cav/cScripts/releases/latest'
        with urllib.request.urlopen(url) as response:
            code = response.getcode()
            raw_json = json.loads(response.read())

            #with open('getlatest.json','w') as outfile:
            #    json.dump(data,outfile)
        
        if(code != 200):
            print("  HTTP Response: {}".format(code))
    else:
        print("not live, reading from file")
        with open('getlatest.json') as json_file:
            raw_json = json.load(json_file)
    
    data['tag_name'] = raw_json['tag_name']
    for asset in raw_json['assets']:
        if(str.startswith(asset['name'],'cScripts-')):
            data['zipUrl'] = asset['browser_download_url']
            data['zipName'] = asset['name']

    print("  Latest cScripts version: {}".format(data['tag_name']))
    
    return data #all json

def download(data):
    # json download_url, zip file name
    live = True
    
    files = os.listdir(scriptpath)
    if(data['zipName'] in files):
        print("  Already have latest version")
    else:
        print("  Downloading...".format(data['zipUrl']))
        if(live):
            urllib.request.urlretrieve(data['zipUrl'],data['zipName'])
        else:
            print("not live, skipping")
    
    extract(data)

def extract(data):
    print("  Extracting zip...")
    os.chdir(projectpath)
    
    clear_folder(cscriptspath)
    #if(os.path.isdir(cscriptspath)):
    #    ctmp = tempfile.mkdtemp()
    #    print("ctmp: {}".format(ctmp))
    #    shutil.move(cscriptspath, ctmp)
    #    shutil.rmtree(ctmp)
    #
    #os.mkdir("cScripts")
    
    os.chdir(scriptpath)
    with zipfile.ZipFile(data['zipName'],'r') as zip_ref:
        zip_ref.extractall(cscriptspath)
    
    #modify init.sqf
    print("  Modifying init.sqf")
    os.chdir(cscriptspath)
    with open("init.sqf", "a") as f:
        f.write("\n// Added by Raynor\n{[_x] execVM 'scripts\\aircraftWarningLights.sqf'} foreach allMissionObjects 'Land_LampHalogen_F';\n")
    
    # modify description.ext
    f = open("description.ext", "r")
    contents = f.readlines()
    f.close()
    
    authorStr = "/*=================== D O   N O T   E D I T"
    authorIndex = 0
    index = 0
    for l in contents:
        index += 1
        if(str.startswith(l,authorStr)):
            authorIndex = index - 2
        if(str.startswith(l,'    class CfgFunctions')):
            break
    
    print("  Modifying description.ext at line {}".format(index))
    contents.insert(index, "        // Added by Raynor\n        #include \"RaynorsTeleporter\\cfgFunctions.hpp\"\n\n")
    
    include = "#include \"author.hpp\""
    
    del contents[:authorIndex]
    contents.insert(0,include)

    f = open("description.ext", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()
    
def copy_file(file,pathSrc,pathDest):
    print("  Copying {} ...".format(file))
    shutil.copy(os.path.join(pathSrc,file),os.path.join(pathDest,file))
    time.sleep(0.25)
    return

def copy(data):
    print("  Copying into files...")
    
    filespath = os.path.join(projectpath,"files")

    os.chdir(projectpath)
    time.sleep(0.25)
    
    # copy cScripts folder
    if(os.path.isdir(os.path.join(filespath,"cScripts"))):
        shutil.rmtree(os.path.join(filespath,"cScripts"))
        
    time.sleep(0.25)
    
    print("  Copying mission/cScripts ...")
    shutil.copytree(os.path.join(cscriptspath,"cScripts"),os.path.join(filespath,"cScripts"))
    
    time.sleep(0.25)
    
    # copy files
    copy_file("cba_settings.sqf",cscriptspath,filespath)
    copy_file("initServer.sqf",cscriptspath,filespath)
    copy_file("init.sqf",cscriptspath,filespath)
    copy_file("description.ext",cscriptspath,filespath)

    os.chdir(filespath)
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'cScripts-*'):
            os.remove(file)
            time.sleep(0.25)
    
    os.chdir(cscriptspath)
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'cScripts-*'):
            print("  Copying mission/{} ...".format(file))
            shutil.copy(os.path.join(cscriptspath,file),os.path.join(filespath,file))
    time.sleep(0.25)
    print("  ===== cScripts updated. Reminder: init.sqf and description.ext have been modified, do not manually overwrite them without merging conflicts.")
    
    return

if __name__ == '__main__':
    print("""
  #################################################
  # A/1-7 Development Environment cScripts Module #
  #################################################

  This script downloads and installs the latest cScripts release in the A/1-7 training mission.
  
  """)
    
    data = getLatest()
    download(data)
    copy(data)

# git repo functions, no longer used
#def get_last_release():
#
#    os.chdir(cscriptspath)
#    subprocess.check_output(["git", "config", "--global", "advice.detachedHead","false"])
#    commit_id = subprocess.check_output(["git", "rev-list", "--tags", "--max-count=1"])
#    commit_id = str(commit_id, "utf-8")[:8]
#    tag_text = subprocess.check_output(["git", "describe", "--tags", commit_id])
#    tag_text = str(tag_text, "utf-8")[:8]
#
#    return commit_id.strip(), tag_text.strip()
#
#def pull():
#    # Checkout latest cScripts release
#    print("  ===== Checking out latest cScripts release")
#
#    commit_id, tag_text = get_last_release();
#
#    subprocess.check_output(["git", "checkout", commit_id])
#
#    print("  ===== Pulled cScripts latest release: {}".format(tag_text))
