# A/1-7 Training Missions

### 1. Requirements
- Python 3
- Arma 3 Tools (optional)

### 2. Development
1. Clone repo to your computer
2. Run [/setup_dev.py](setup_dev.py)
3. Make and test desired changes

- Missions can be accessed in Eden under **7Cav A-1-7**
- Modify mission files inside the [/files](https://github.com/RaynorD/Alpha_1-7_Training/tree/master/files) folder
- **You cannot use Export > Export to Multiplayer in Eden to build PBOs from the symlinked files. Any files in folders will not be copied to the pbo.**

### 3. Maintenance
- To update cScripts, copy all files in the cScripts release **except init.sqf and description.ext** into the [/files](https://github.com/RaynorD/Alpha_1-7_Training/tree/master/files) directory. These files have been modified for this mission. If those files are updated in cScripts, you'll need to merge the changes.

### 3. Building a Release
1. Run [/build_release.py](build_release.py) (requires Arma 3 tools)
2. Copy zip from [/release](https://github.com/RaynorD/Alpha_1-7_Training/tree/master/release) for dedicated testing and release.
