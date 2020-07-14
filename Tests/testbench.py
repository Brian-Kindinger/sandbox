import sys
from pathlib import *

# Dynamically import ResourceMgr from another location.  Path is testbench.py/../lib
sys.path.append("c:\\Git\\sandbox\\lib")
import ResourceMgr

def main():
    print("Program Started")
    RMgr=ResourceMgr.ResrcMgr()
    RMgr.newResrcMapFromHardwareDescription(Path.cwd() / "myfirstresourcemap.json")

    f = open(Path.cwd() / "myresources.rsc", "w")
    f.write(str(RMgr.resources))
    f.close()


if __name__ == "__main__":
    main()