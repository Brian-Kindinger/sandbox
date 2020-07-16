import json
import uuid
from pathlib import Path

class ResrcMgr:
    resrcMap = None

    def __init__(self):
        print ("Resource Manager initialized")

    def newResrcMapFromHardwareDescription(self, filepath):
        HardwareDescription = json.load(open(filepath, "r"))
        self.resrcMap = HardwareDescription["resources"].copy()
        classBasePath = Path(__file__).parents[1] / "classes"
        for resource in self.resrcMap:
            if "scope" not in resource:
                resource["scope"] = HardwareDescription["defaultscope"]
            classToMerge = json.load(open(classBasePath / (resource["class"] + ".json"), "r"))
            resource["inports"]=classToMerge["inports"].copy()
            resource["outports"]=classToMerge["outports"].copy()
            resource["configItems"]=[]
            for configItem in classToMerge["configItems"]:
                rsrcConfigItem=dict()
                rsrcConfigItem["GUID"] = str(uuid.uuid4())
                rsrcConfigItem["name"] = configItem
                rsrcConfigItem["value"] = classToMerge["configItems"][configItem]
                resource["configItems"].append(rsrcConfigItem.copy())           
        return self.resrcMap

    def saveResrcMap(self, filepath):
        f = open(filepath, "w")
        prettyJsonResrcMap = json.dumps(self.resrcMap, indent=4)
        f.write(prettyJsonResrcMap)
        f.close()
        return 0

    def loadResrcMap(self, filepath):
        f = open(filepath, "r")
        jsonResrcMap = f.read()
        self.resrcMap = json.loads(jsonResrcMap)
        f.close()
        return 0

    def getConfigItemByGuid(self, GUID):
        for resource in self.resrcMap:
            for configItem in resource["configItems"]:
                if (configItem["GUID"] == GUID): return json.dumps(configItem, indent=4)
        return -1

    def setConfigItemValueByGuid(self, GUID, value):
        for resource in self.resrcMap:
            for configItem in resource["configItems"]:
                if (configItem["GUID"] == GUID):
                    configItem["value"]= value 
                    return 1
        return -1

    def getConfigItemByName(self, name):
        for resource in self.resrcMap:
            for configItem in resource["configItems"]:
                if (configItem["name"] == name): return configItem
        return -1

    def getDescription(self):
        return self.resrcMap("description")
