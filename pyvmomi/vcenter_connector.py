from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

class VCenterConnector:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.si = None

    def connect(self):
        # Proper SSL Context setup and connection handling
        try:
            context = ssl._create_unverified_context()
            self.si = SmartConnect(host=self.host, user=self.user, pwd=self.password, sslContext=context)
        except vim.fault.InvalidLogin as e:
            raise ConnectionError("Invalid vCenter credentials") from e
        except ssl.SSLError as e:
            raise ConnectionError("SSL Certificate error") from e
        except Exception as e:
            raise ConnectionError("Unexpected error occurred") from e

    def disconnect(self):
        if self.si:
            Disconnect(self.si)
