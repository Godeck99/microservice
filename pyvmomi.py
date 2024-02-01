from fastapi import FastAPI, HTTPException
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect
import sys

app = FastAPI()

# Function to connect to the vCenter
def get_vcenter_connection(host, user, password):
    try:
        service_instance = SmartConnectNoSSL(host=host, user=user, pwd=password)
        return service_instance
    except vim.fault.InvalidLogin:
        raise HTTPException(status_code=401, detail="Invalid vCenter credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to find a specific VM by its name
def get_vm_by_name(service_instance, vm_name):
    content = service_instance.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in container.view:
        if vm.name == vm_name:
            return vm
    return None

@app.get("/vm/{vm_name}")
async def list_vm(vm_name: str, host: str, user: str, password: str):
    service_instance = get_vcenter_connection(host, user, password)
    if service_instance:
        vm = get_vm_by_name(service_instance, vm_name)
        Disconnect(service_instance)
        if vm:
            return {"vm_name": vm.name, "vm_status": vm.runtime.powerState}
        else:
            raise HTTPException(status_code=404, detail="VM not found")
    else:
        raise HTTPException(status_code=500, detail="Could not connect to vCenter")