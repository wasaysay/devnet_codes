from netmiko import ConnectHandler
from datetime import datetime

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

with ConnectHandler(**hillstone1) as net_connect:
    cmd_list = [
        "save\n",
        "y",
        "y",
    ]

    # "normalize = False", don't Enter after command. So must add "\n" after "save".
    start_time = datetime.now()
    output = net_connect.send_multiline_timing(cmd_list, normalize=False)
    end_time = datetime.now()

print()
print(output)
print(f"exec time is {end_time - start_time}")
print()