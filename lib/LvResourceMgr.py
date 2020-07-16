import ResourceMgr
import json

RMgr = ResourceMgr.ResrcMgr()

def lvNewResrcMapFromHardwareDescription(filename):
    RMgr.newResrcMapFromHardwareDescription(filename)
    return 0

def lvSaveResrcMap(filename):
    RMgr.saveResrcMap(filename)
    return 0

def lvLoadResrcMap(filename):
    RMgr.loadResrcMap(filename)
    return 0

def lvInspectResrcMap():
    return json.dumps(RMgr.resrcMap, indent=4)

def lvGetConfigItemByGuid(GUID):
    return RMgr.getConfigItemByGuid(GUID)

def lvSetConfigItemValueByGuid(GUID, value):
    RMgr.setConfigItemValueByGuid(GUID, value)
    return 0

def version():
    return "1"

