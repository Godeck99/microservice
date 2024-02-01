# vcenter_operations.py
from pyVmomi import vim

class VCenterOperations:
    def __init__(self, service_instance):
        self.si = service_instance

    def get_vm_by_name(self, vm_name):
        content = self.si.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        for vm in container.view:
            if vm.name == vm_name:
                return self._collect_vm_details(vm)
        return None

    def get_all_vms(self):
        content = self.si.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        vms = []
        for vm in container.view:
            vms.append(self._collect_vm_details(vm))
        return vms

    def _collect_vm_details(self, vm):
        summary = vm.summary
        vm_details = {
            'vm_name': summary.config.name,
            'storage_used': summary.storage.committed,
            'host_name': summary.runtime.host.name,
            'vm_status': summary.runtime.powerState,
            # Add more details as needed
        }
        return vm_details
