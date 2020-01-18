# A/1-7 Training Missions

### 1. Requirements
- Python 3
- Arma 3 Tools

### 2. Development
1. Clone repo to your computer
2. Run [tools/setup_dev.py](tools/setup_dev.py)
3. Make and test desired changes

- Missions can be accessed in Eden under **7Cav A-1-7**
- Modify mission files inside the [/files](https://github.com/RaynorD/Alpha_1-7_Training/tree/master/files) folder
- **You cannot use Export > Export to Multiplayer in Eden to build PBOs from the symlinked files. Any files in folders will not be copied to the pbo.**

### 3. Building a Release
1. Run [tools/build_release.py](tools/build_release.py) (requires Arma 3 tools)
2. Copy zip from [/release](https://github.com/RaynorD/Alpha_1-7_Training/tree/master/release) for dedicated testing and release.

## Maintenance
### Updating cScripts
1. Run [tools/cScripts.py](tools/cScripts.py)

### Adding a new map
1. Start a new mission on the desired map
2. Merge in one of the current missions and adapt the objects
3. Save it **but not in A-1-7**, name doesn't matter
4. In Eden, go to Scenario > Open Scenario Folder
5. Copy mission.sqm into the repo under [/sqm](https://github.com/RaynorD/Alpha_1-7_Training/tree/master/sqm)
6. Rename mission.sqm to (mapname).sqm (the scenario folder will end with it)
7. Run [tools/setup_dev.py](tools/setup_dev.py) again
8. Open the mission, now in the A-1-7 folder, and continue editing
