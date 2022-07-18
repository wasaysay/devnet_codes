# WMI info
#https://docs.microsoft.com/en-us/windows/desktop/cimwin32prov/win32-networkadapterconfiguration
#https://www.cnblogs.com/mcafee/p/5198670.html
if __name__ == '__main__':


    import wmi
    import pywin
    c = wmi.WMI()


    print("startted..")
    for os in c.Win32_OperatingSystem():
        print(os.Caption)
    nics=c.Win32_NetworkAdapterConfiguration(IPEnabled=True)

    for objinnics in nics:
       if objinnics.Description=="Intel(R) Ethernet Connection I219-V":
            print(objinnics.IPaddress)
            ipaddr=['192.168.1.100']
            netmask=['255.255.255.0']
            returnvalue= objinnics.EnableStatic(IPAddress=ipaddr,SubnetMask=netmask)
            print(returnvalue[0])
            if returnvalue[0]==0:
                print("Successful")
            else:
                print('failed')
