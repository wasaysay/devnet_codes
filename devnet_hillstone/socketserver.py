import socket
import json
serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serversocket.bind(('127.0.0.1',9999))

serversocket.listen(5)

while True:
    clientsocket, addr = serversocket.accept()
    with open("password.txt", 'r') as fo:
        load_dict = json.load(fo)
        username = load_dict['username']
        password = load_dict['password']

    msg = str(username + ',' + password)
    clientsocket.send(msg.encode('utf-8'))
    clientsocket.close()
    fo.close()
    print("sent username and password successfully")