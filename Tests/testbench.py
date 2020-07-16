import sys
from pathlib import Path

# Dynamically import ResourceMgr from another location.  Path is testbench.py/../lib
sys.path.append("c:\\Git\\sandbox\\lib")
import ResourceMgr

def main():
    actions = ["NewAndSave", "LoadOnly"]
    actionToDo = actions[0]
    print("Program Started")
    RMgr=ResourceMgr.ResrcMgr()

    if actionToDo is "NewAndSave":
        RMgr.newResrcMapFromHardwareDescription(Path.cwd() / "myfirstresourcemap.json")
        RMgr.saveResrcMap(Path.cwd() / "myresources1.rsm")
    elif "LoadOnly":
        RMgr.loadResrcMap(Path.cwd() / "myresources1.rsm")
        RMgr.saveResrcMap(Path.cwd() / "myresources2.rsm")
    else:
        print("Bad Action to do")

    print("Done")

if __name__ == "__main__":
    main()