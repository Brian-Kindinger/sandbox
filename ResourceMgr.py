import json


class ResrcMgr:
    resources = None

    def __init__(self,filepath):
        f = open(filepath, "r")
        self.resources = json.load(f)


