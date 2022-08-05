from netmiko import ConnectHandler
from datetime import datetime
import IPy
key_file = r"C:\Users\Eden\.ssh\openssh"

hillstone1 = {
    "device_type": "hillstone",
    "host": "10.0.0.253",
    "port": "22",
    "username": "hillstoneapi",
    "use_keys": True,
    "key_file": key_file,
    "session_log": "output.txt",
    # Disable algorithms for Hillstone devices.. the following two are not supported in Hillstone SSHD (debug sshd).
    # See https://www.5axxw.com/questions/content/2l1peh
    # This option can be found in base_connection.py
    "disabled_algorithms": dict(pubkeys=["rsa-sha2-512","rsa-sha2-256"]),
}

i = 0
ip = IPy.IP('1.0.0.0/8')
output = ""
with ConnectHandler(**hillstone1) as net_connect:
    net_connect.config_mode()
    start_time = datetime.now()
    while True:
        cmd_list = [
            [f"tunnel ipsec ipsec{i} auto", "#"],
            ["exit", "#"],
            ["interface tunnel1", "#"],
            [f"tunnel ipsec ipsec{i} gw {ip[i]}", "#"],
            ["exit", "#"],
        ]
        try:
            output = net_connect.send_multiline(cmd_list)
        except Exception as e:
            print(f"maximum ipsec tunnels number is {i}")
            print(e)
            break
        i += 1

    end_time = datetime.now()
print()
print(output)
print(f"exec time is {end_time - start_time}")