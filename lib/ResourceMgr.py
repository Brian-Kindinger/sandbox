import json
import uuid
from pathlib import Path

class ResrcMgr:
    resources = None
    description = None

    def __init__(self):
        print ("Resource Manager initialized")

    def newResrcMapFromHardwareDescription(self, filepath):
        HardwareDescription = json.load(open(filepath, "r"))
        self.resources = HardwareDescription["resources"].copy()
        self.description = HardwareDescription["description"]
        classBasePath = Path(__file__).parents[1] / "classes"
        for resource in self.resources:
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
        return self.resources

    def getConfigItemByGuid(self, GUID):
        for resource in self.resources:
            for configItem in resource["configItems"]:
                if (configItem["GUID"] == GUID): return configItem
        return -1

    def getConfigItemByName(self, name):
        for resource in self.resources:
            for configItem in resource["configItems"]:
                if (configItem["name"] == name): return configItem
        return -1

    def getDescription(self):
        return self.description

    def getResources(self):
        return self.resources


