import json
import sys
import uuid
from pathlib import Path

class ResrcMgr:
    resrcMap = {"resources":[]}

    def __init__(self):
        print ("Resource Manager initialized")

    def newResrcMapFromHardwareDescription(self, filepath):
        HardwareDescription = json.load(open(filepath, "r"))   
        if "multiscope" in HardwareDescription:
            for newscope in HardwareDescription["multiscope"]:
                tempResources = HardwareDescription["resources"].copy()
                for tempResource in tempResources:
                    tempResource["scope"] = newscope
                    self.resrcMap["resources"].append(tempResource.copy())
        else:
            self.resrcMap["resources"] = HardwareDescription["resources"].copy()
        templateBasePath = Path(__file__).parents[0] / "templates"
        for resource in self.resrcMap["resources"]:
            templateToMerge = json.load(open(templateBasePath / (resource["template"] + ".json"), "r"))
            if "scope" not in resource:
                resource["scope"] = HardwareDescription["defaultscope"]
            if "version" in templateToMerge:
                resource["version"] = templateToMerge["version"]
            else:
                resource["version"] = 1
            resource["inports"]=templateToMerge["inports"].copy()
            resource["outports"]=templateToMerge["outports"].copy()
            resource["configItems"]=[]
            for configItem in templateToMerge["configItems"]:
                rsrcConfigItem=dict()
                rsrcConfigItem["GUID"] = str(uuid.uuid4())
                rsrcConfigItem["name"] = configItem
                rsrcConfigItem["value"] = templateToMerge["configItems"][configItem]
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
        self.mutateResources()
        return 0

    def mutateResources(self):
        mutator = defaultMutator()
        for resource in self.resrcMap["resources"]:
            if mutator.readyForMutation(resource): mutator.mutate(resource)
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

class defaultMutator:

    def __init__(self):
        print("Default mutation started")

    def readyForMutation(self, resource):
        if "version" not in resource:
                versionNumber=1
        else:
            versionNumber = resource["version"]
        template = self.getTemplate(resource)
        if "version" not in template:
            return False
        else:
            return (template["version"] != versionNumber)

    def mutate(self, resource):
        template = self.getTemplate(resource)
        resource["version"] = template["version"]

        if "inports" in template: resource["inports"] = template["inports"]
        if "outports" in template: resource["outports"] = template["outports"]
        #remove unneeded keys
        for configItem in resource["configItems"]:
            if configItem["name"] not in template["configItems"]:
                resource["configItems"].remove(configItem)
        #add new keys
        for key,value in template["configItems"].items():
            configItemNames = []
            for configItem in resource["configItems"]:
                configItemNames.append(configItem["name"])
            if key not in configItemNames:
                newConfigItem = dict()
                newConfigItem["GUID"] = str(uuid.uuid4())
                newConfigItem["name"] = key
                newConfigItem["value"] = value
                resource["configItems"].append(newConfigItem.copy())
        return 0

    def getTemplate(self, resource):
        templatePath = str(Path(__file__).parents[0] / "templates" / resource["template"]) + ".json"
        template = json.load(open(templatePath, "r"))
        return template