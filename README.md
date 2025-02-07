
<img src="https://github.com/muonium-ai/unify/blob/main/images/logo.webp" alt="Unify Logo" width="200"/>

# unify
single file / binary for unifying file for code repos to be used with LLM

## features
- single python file, 
- no pip dependency
- less than 100 lines(82 now)

## inspired by repomix


## steps

download the unify.py script to your folder and run if you already have python installed

for reducing token size, create a .unity file in your repo or folder and ignore binary files, build files, to it, in add section which files matter to you

### usage
python unify.py repo-path

if you do not have a build you can download the executable created with pyinstaller, windows only for now as dont have mac/ubuntu with me now

you can create your own executable 

`pip install pyinstaller`

`pyinstaller --onefile --icon=images/logo.ico unify.py`

binary will be in the dist/ folder

with binary

`unify.exe repo-path`

for this repo
`.\dist\unify\unify.exe .
Total Files: 4
Total Lines: 177
Total Word Count: 485
Repository packed into C:\Users\senthil\unify\unify-output.txt`