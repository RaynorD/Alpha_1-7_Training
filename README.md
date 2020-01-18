# A/1-7 Training Missions

### 1. Requirements
- Python 3
- Arma 3 Tools (optional)

### 2. Development
1. Run [/setup_dev.py](setup_dev.py)
2. Make and test desired changes

### 3. Testing on Dedicated Server
1. Run [/build_test_release.py](build_test_release.py) (requires Arma 3 tools)
2. Copy pbos from [/pbo](https://github.com/RaynorD/Alpha_1-7_Training/tree/master/pbo) to server and test

### 4. Pushing a Release
1. Ensure changes have been pushed/merged to master branch
2. Create a tag on the master branch named the new version (vX.X.X)
3. (Automatic) PBOs are built via Github action (suffixed with tag name)
4. (Automatic) Zip is packed and uploaded as release (named same as tag)
5. Send release zip to S6 for upload
