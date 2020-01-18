# not used right now

import os
import configparser
from pathlib import Path
import subprocess
import fileinput

scriptpath = Path(os.path.realpath(__file__))

projectpath = scriptpath.parent.parent
print("Project Path: {}".format(projectpath))

inipath = os.path.join(projectpath,"edits.ini")

config = configparser.ConfigParser(strict=False)
config.read(inipath)

sections = config.sections()

for file in config.sections():
    print("Making edit in {}".format(file))
    
    f = open(os.path.join(projectpath,"files",file), "r")
    contents = f.readlines()
    f.close()
    print("Read {} with {} lines".format(file,len(contents)))
    
    contents_stripped = []
    for line in contents:
        contents_stripped.append(line.strip())
    
    line = config[file]['line']
    if('after' in config[file]):
        print("Inserting {}".format(line))
        after = config[file]['after']
        print("    After: {}".format(after))
        linenum = contents_stripped.index(after)
        print("Inserting line at line #{}".format(linenum))
        contents.insert(linenum+1,line)
    else:
        print("Appending {}".format(line))
        contents.append(line)
    
    for line in contents:
        print(line)
    
