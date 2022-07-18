# WMI info
#https://docs.microsoft.com/en-us/windows/desktop/cimwin32prov/win32-networkadapterconfiguration
#https://www.cnblogs.com/mcafee/p/5198670.html

import wmi
import time
c = wmi.WMI()
nics=c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
for objinnics in nics:
    if objinnics.Description == "Intel(R) Ethernet Connection I219-V":
        print(objinnics.IPaddress)
        returnvalue = objinnics.EnableDHCP()
        if returnvalue[0] == 0:
            print("Successful")
            time.sleep(5)
            print(objinnics.IPaddress)
        else:
            print('failed')