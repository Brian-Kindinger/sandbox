import sys
from pathlib import Path

# Dynamically import ResourceMgr from another location.  Path is testbench.py/../lib
sys.path.append("c:\\Git\\sandbox\\lib")
import ResourceMgr

def main():
    print("Program Started")
    RMgr=ResourceMgr.ResrcMgr()
    RMgr.newResrcMapFromHardwareDescription(Path.cwd() / "myfirstresourcemap.json")

    RMgr.saveResrcMap(Path.cwd() / "myresources.rsm")
    
    RMgr2=ResourceMgr.ResrcMgr()
    RMgr2.loadResrcMap(Path.cwd() / "myresources.rsm")
    print("Done")

if __name__ == "__main__":
    main()