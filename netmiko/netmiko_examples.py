from netmiko import ConnectHandler
from getpass import getpass

"""Use getpass to input the password, but it only works in terminal via python netmikoexample.py"""
password = getpass()

hillstone1 = {
    "device_type": "hillstone",
    "host": "10.0.0.1",
    "port": "2233",
    "username": "hillstone",
    "password": password,
    "session_log": "output.txt"
}

with ConnectHandler(**hillstone1) as net_connect:

    """Example of adding static route via write_channel()"""
    net_connect.config_mode()
    net_connect.write_channel("ip vrouter trust-vr")
    net_connect.write_channel(net_connect.RETURN)
    net_connect.write_channel("ip route 1.1.1.1/32 10.0.0.2")
    net_connect.write_channel(net_connect.RETURN)
    net_connect.exit_config_mode()

    """Example of sending show command."""
    output = net_connect.send_command("show ip route 1.1.1.1")

    """
    Example of configuration changes via send_config_set()
    Netmiko will automatically enter and exit config mode
    """

    output += net_connect.send_config_set("admin host 1.1.1.1/32 ssh")

    config_set = [
        "ip vrouter trust-vr",
        "ip route 2.2.2.2/32 10.0.0.2",
    ]
    output += net_connect.send_config_set(config_set)

    """Example of save configurations"""
    output += net_connect.save_config()

print()
print(output)
print()

