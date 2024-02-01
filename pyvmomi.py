from fastapi import FastAPI, HTTPException
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
import ssl

app = FastAPI()

# Function to connect to the vCenter with SSL verification
def get_vcenter_connection(host, user, password):
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.verify_mode = ssl.CERT_REQUIRED
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
            return {"vm_name": vm.name, "vm_status": vm.runtime.powerState}
    return None

@app.get("/vm/{vm_name}")
async def list_vm(vm_name: str, host: str, user: str, password: str):
    service_instance = None
    try:
        service_instance = get_vcenter_connection(host, user, password)
        vm_details = get_vm_by_name(service_instance, vm_name)
        if vm_details:
            return vm_details
        else:
            raise HTTPException(status_code=404, detail="VM not found")
    except HTTPException as http_exc:
        # Re-raise the HTTPException to be handled by FastAPI
        raise http_exc
    finally:
        # Ensure we always disconnect, even if the above code raises an exception
        if service_instance:
            Disconnect(service_instance)