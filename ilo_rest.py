import json
import request
import requests
import urllib3
import pymongo
#Quitar Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#configurar nombre de Server
server_redfish="https://ilorestfulapiexplorer.ext.hpe.com/"

#general=open("Mem.json").read()
#data = json.loads(general)
#json.dumps(json.loads(response.text), indent=4, sort_keys=True))

def load_file_json(file):
        __openfile=open(file).read()
        return json.loads(__openfile)
def print_json(objeto):
        print(json.dumps(objeto, indent=4, sort_keys=True))
        return
def get_mem_info(dimms,num_processors):
        _mem={}
        _mem_total={}
        #_server=json.loads(requests.get(server_redfish+"/redfish/v1/Systems/1/Memory/"),verify=False)
        for x in range(num_processors):
                for y in range(dimms-12):
                        r = requests.get(server_redfish+"/redfish/v1/Systems/1/Memory/proc"+str(x+1)+"dimm"+str(y+1),verify=False)
                        objeto_json=json.loads(r.text)
                        if objeto_json["Status"]["State"]=="Enabled":
                                _id=objeto_json["DeviceLocator"]
                                _mem[_id]={}
                                _mem[_id]["BaseModuleType"] = objeto_json["BaseModuleType"]
                                _mem[_id]["CapacityMiB"] = objeto_json["CapacityMiB"]
                                _mem[_id]["DeviceLocator"]=objeto_json["DeviceLocator"]
                                _mem[_id]["Manufacturer"]=objeto_json["Manufacturer"]
                                _mem[_id]["MemoryDeviceType"]=objeto_json["MemoryDeviceType"]
                                _mem[_id]["PartNumber"]=objeto_json["PartNumber"]
                                _mem[_id]["DataWidthBits"]=objeto_json["DataWidthBits"]
                                _mem_total.update(_mem)
        return _mem_total

def get_nic_info(num_nics):
        _nic={}
        _nic_total={}
        r = requests.get(server_redfish+"/redfish/v1/Systems/1/BaseNetworkAdapters/1",verify=False)
        objeto_json=json.loads(r.text)
        _nic["_id"]=objeto_json["Id"]
        _nic["Name"]=objeto_json["Name"]
        _nic["PhysicalPorts"]=objeto_json["PhysicalPorts"]
        return _nic

def get_system_info():
        #_system_temp=requests.get(server_redfish+"/redfish/v1/Systems/1",verify=False)
        _system={}
        _system_total={}
        r = requests.get(server_redfish+"/redfish/v1/Systems/1",verify=False)
        objeto_json=json.loads(r.text)
        _id=objeto_json["SerialNumber"]
        _system[_id]={}
        _system[_id]["PartNumber"]=objeto_json["SKU"]
        _system[_id]["Model"]=objeto_json["Model"]
        _system[_id]["BiosVersion"]=objeto_json["BiosVersion"]
        _system[_id]["HostName"]=objeto_json["HostName"]
        _system[_id]["Manufacturer"]=objeto_json["Manufacturer"]
        _system[_id]["TotalMemory"]=objeto_json["MemorySummary"]["TotalSystemMemoryGiB"]
        _system[_id]["BoardPartNumber"]=objeto_json["Oem"]["Hpe"]["PCAPartNumber"]
        _system[_id]["BoardSerialNumber"]=objeto_json["Oem"]["Hpe"]["PCASerialNumber"]
        _system[_id]["ProcessorCount"]=objeto_json["ProcessorSummary"]["Count"]
        _system["ProcessorModel"]=objeto_json["ProcessorSummary"]["Model"]
        _system["SerialNumber"]=objeto_json["SerialNumber"]
        _system["UUID"]=objeto_json["UUID"]
        return _system

#data=open("Nic.json").read()
#x=json.loads(data)
#print_json(x)
#print(type(x))
#y=x["PhysicalPorts"]
#print(type(y))
#print(x["PhysicalPorts"])
#print(x["Members@odata.count"])
#test=get_mem_info(24,2)
#test2=get_nic_info(4)
#test3=get_system_info()
#print_json(test3)
#print_json(test)
server="Server1"
ilo={}
ilo[server]={}
ilo[server]["System"]=get_system_info()
ilo[server]["Memory"]=get_mem_info(24,2)
ilo[server]["Nic"]=get_nic_info(2)

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#mydb = myclient["ilo"]
#dblist = myclient.list_database_names()
#print(dblist)
#mycol = mydb["Clientes"]

#print(mydb.list_collection_names())
#x = mycol.insert_one(ilo)



print_json(ilo)

