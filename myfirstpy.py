import ResourceMgr
from pathlib import Path

def main():
    print("Program Started")
    y=ResourceMgr.ResrcMgr(Path.cwd() / "myfirstresourcemap.json")
    print(y.resources["nodes"])

if __name__ == "__main__":
    main()