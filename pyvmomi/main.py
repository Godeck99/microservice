# Now, the API module (main.py) will use the VCenterOperations class.
from fastapi import FastAPI, HTTPException
from config import VCENTER_HOST, VCENTER_USER, VCENTER_PASSWORD
from vcenter_connector import VCenterConnector
from vcenter_operations import VCenterOperations

app = FastAPI()

@app.get("/vm/{vm_name}")
def get_vm_details(vm_name: str):
    connector = VCenterConnector(VCENTER_HOST, VCENTER_USER, VCENTER_PASSWORD)
    try:
        connector.connect()
        operations = VCenterOperations(connector.si)
        vm_details = operations.get_vm_by_name(vm_name)
        if vm_details is None:
            raise HTTPException(status_code=404, detail="VM not found")
        return vm_details
    except ConnectionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connector.disconnect()

@app.get("/vms")
def get_all_vms():
    connector = VCenterConnector(VCENTER_HOST, VCENTER_USER, VCENTER_PASSWORD)
    try:
        connector.connect()
        operations = VCenterOperations(connector.si)
        all_vms = operations.get_all_vms()
        return all_vms
    except ConnectionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connector.disconnect()
