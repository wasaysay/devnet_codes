import paramiko
import time

ip = '10.0.0.1'
username = 'hillstone'
password = 'hillstone'
sshport = 2233

ssh_client = paramiko.SSHClient()
# auto add unknown ssh public keys
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip,username=username,password=password,port=sshport,look_for_keys=False)
command = ssh_client.invoke_shell()

print("login to device", ip, "successfully!")

# For hillstone device, must add timing 1s at least!

time.sleep(1)
command.send('configure\n')
time.sleep(1)
command.send('interface loopback8\n')
time.sleep(1)
command.send('zone trust\n')
time.sleep(1)
command.send('ip address 2.2.2.2/32\n')
time.sleep(1)
command.send('end\n')
time.sleep(1)
command.send('save\n')
time.sleep(1)
command.send('y')
time.sleep(1)
command.send('y')

time.sleep(1)

# change to utf-8 for Chinese
output = command.recv(65535).decode('ascii')
print(output)

ssh_client.close()
