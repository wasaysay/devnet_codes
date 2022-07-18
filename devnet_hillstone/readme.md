## Socketserver.py

Listen on port 9999 and send the username and password saved in the file <password.txt> to the client.

## Socketclient.py

1. connect to server on port 9999
2. recv username and password
3. login to hillstone firewall via restapi and get cpu utilization of 1minute
4. If the cpu utilization of 1 minute exceeds the threshold 50 then 
   - send a mail to  327105204@qq.com with hostname and SN 
   - save the hostname, SN and timestamp to the database



