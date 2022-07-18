import re


def printdot10(ip):
    ip[0] = int(ip[0], 16)
    ip[1] = int(ip[1], 16)
    ip[2] = int(ip[2], 16)
    ip[3] = int(ip[3], 16)
    print("%d.%d.%d.%d" % (ip[0], ip[1], ip[2], ip[3]))


data = "x"
while (data != "exit"):
    print("Please input the hex (format : c0a80100 ffffff00)")
    data = input()
    # data= "c0a80100 ffffff00"
    srcstr = data.split()

    ip = re.findall(r'.{2}', srcstr[0])
    mask = re.findall(r'.{2}', srcstr[1])

    printdot10(ip)
    printdot10(mask)
    print("=================")
