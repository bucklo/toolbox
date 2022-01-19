#!/usr/bin/python
from __future__ import absolute_import, division, print_function
from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl

__metaclass_ = type


class smhi_vmware:
    def __init__(self, provider):
        host = provider["host"]
        user = provider["user"]
        pwd = provider["pwd"]

        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        s.verify_mode = ssl.CERT_NONE

        try:
            self.handle = SmartConnect(host=host, user=user, pwd=pwd)
            print("Valid certificate")
        except:
            self.handle = SmartConnect(host=host, user=user, pwd=pwd, sslContext=s)
            print("Invalid certificate")

        self.content = self.handle.RetrieveContent()

    def get_vmhost(self, hostname):
        host_view = self.content.viewManager.CreateContainerView(
            self.content.rootFolder, [vim.HostSystem], True
        )
        for host in host_view.view:
            if host.name == hostname:
                return host

    def get_vmhost_advancedSetting(self, hostname, advancedSetting):
        host = self.get_vmhost(hostname)
        optionManager = host.configManager.advancedOption
        for x in optionManager.setting:
            if x.key == advancedSetting:
                return x.value

    def set_vmhost_advancedSetting(self, hostname, advancedSetting, value):
        host = self.get_vmhost(hostname)
        optionManager = host.configManager.advancedOption
        option = vim.option.OptionValue(key=advancedSetting, value=value)
        optionManager.UpdateOptions(changedValue=[option])

    def get_datastore(self, datastore_name):
        content = self.handle.RetrieveContent()
        datastore_view = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.Datastore], True
        )
        for datastore in datastore_view.view:
            if datastore.name == datastore_name:
                return datastore

    def create_datastore_folder(self, datastore_name, folder):
        datacenter_obj = self.content.rootFolder.childEntity[0]
        fileManager = self.content.fileManager
        folder = f"[{datastore_name}]/{folder}"
        fileManager.MakeDirectory(
            name=folder, datacenter=datacenter_obj, createParentDirectories=True
        )
