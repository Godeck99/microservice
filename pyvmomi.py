from fastapi import FastAPI, HTTPException
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
import ssl
import sys

app = FastAPI()

# Function to connect to the vCenter with SSL verification
def get_vcenter_connection(host, user, password):
    try:
        # Create an SSL context to be used for the connection
        # This context will enforce certificate verification
        ssl_context = ssl.create_default_context()
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        # If necessary, you can specify CA certificates here:
        # ssl_context.load_verify_locations('path/to/ca_certificates')

        service_instance = SmartConnect(host=host, user=user, pwd=password, sslContext=ssl_context)
        return service_instance
    except vim.fault.InvalidLogin:
        raise HTTPException(status_code=401, detail="Invalid vCenter credentials")
    except ssl.SSLError as ssl_error:
        raise HTTPException(status_code=500, detail=f"SSL certificate error: {ssl_error}")
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