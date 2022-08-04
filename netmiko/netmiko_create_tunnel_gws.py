import time

from netmiko import ConnectHandler
import IPy
from getpass import getpass

"""Use getpass to input the password, but it only works in terminal via python file_name.py"""
password = getpass()

hillstone1 = {
    "device_type": "hillstone",
    "host": "10.0.0.1",
    "port": "2233",
    "username": "hillstone",
    "password": password,
    "session_log": "output.txt"
}

ip = IPy.IP('1.0.0.0/8')

with ConnectHandler(**hillstone1) as net_connect:

    # Create interface tunnel1
    net_connect.config_mode()
    net_connect.write_channel("interface tunnel1")
    net_connect.write_channel(net_connect.RETURN)
    net_connect.write_channel("exit")
    net_connect.write_channel(net_connect.RETURN)

    # Create tunnel ipsec and bind to tunnel interface
    for i in range(1000):
        net_connect.write_channel("tunnel ipsec ipsec" + str(i) + " auto")
        net_connect.write_channel(net_connect.RETURN)
        net_connect.write_channel("exit")
        net_connect.write_channel(net_connect.RETURN)
        net_connect.write_channel("interface tunnel1")
        net_connect.write_channel(net_connect.RETURN)
        net_connect.write_channel("tunnel ipsec ipsec" + str(i) + " gw " + str(ip[i]))
        net_connect.write_channel(net_connect.RETURN)
        net_connect.write_channel("exit")
        net_connect.write_channel(net_connect.RETURN)
        time.sleep(1)
