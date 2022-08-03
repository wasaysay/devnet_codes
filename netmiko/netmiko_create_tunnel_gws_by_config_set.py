import time

from netmiko import ConnectHandler
import IPy
from getpass import getpass

"""Use getpass to input the password, but it only works in terminal via python file_name.py"""
#password = getpass()

hillstone1 = {
    "device_type": "hillstone",
    "host": "10.0.0.1",
    "port": "2233",
    "username": "hillstone",
    "password": "Hillstone@123!",
    "session_log": "output.txt"
}

ip = IPy.IP('1.0.0.0/8')
commands_create_tunnel_interface = [
    "interface tunnel1"
]

output = ""
i = 0

with ConnectHandler(**hillstone1) as net_connect:
    # Function send_config_set is much slower than write_channel, since write_channel don't support timming and
    # return values.
    # Create interface tunnel1
    net_connect.send_config_set(commands_create_tunnel_interface)

    # Create tunnel ipsec and bind to tunnel interface, stop the loop when see "Error"
    while True:
        # to handle ipsec tunnel capacity error
        commands_create_ipsec_tunnel_and_bind = [
            "tunnel ipsec ipsec" + str(i) + " auto"
        ]
        output += net_connect.send_config_set(commands_create_ipsec_tunnel_and_bind)

        # stop the loop when see "Error: Exceed maximum number of tunnel" in output.
        if "Error" in output:
            print("Error" + str(i))
            break
        # to bind ipsec tunnels to tunnel interface
        commands_create_ipsec_tunnel_and_bind = [
            "interface tunnel1",
            "tunnel ipsec ipsec" + str(i) + " gw " + str(ip[i]),
            "exit"
        ]
        output += net_connect.send_config_set(commands_create_ipsec_tunnel_and_bind)
        if "Error" in output:
            print("Error")
            break
        i += 1
