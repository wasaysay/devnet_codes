import socket
import requests
import base64
import json
import urllib3
import time
import datetime
from stonehelper import StoneHelper, ConnectionType
import re
import pymysql
from email.mime.text import MIMEText
from email.header import Header
import smtplib


def getBase64code(st):
    return str(base64.b64encode(st.encode("utf-8")), "utf-8")


def login(host, username, password):
    # After login success, return the cookies
    url = str(host) + "/rest/api/login"

    # need base64 encode username and password in newer versions
    base64_username = getBase64code(username)
    base64_password = getBase64code(password)

    # login data
    body = {"lang": "en", 'userName': base64_username, 'password': base64_password}

    # POST login
    s = requests.session()
    req = s.post(url=url, data=json.dumps(body), verify=False)

    # Get login response in dict
    res = req.json()

    if res["success"]:
        print("Login Success!")
        cookie = res["result"][0]
        mycookie = {}
        for key in ["token", "role", "vsysId"]:
            mycookie[key] = cookie[key]
        mycookie["username"] = username
        mycookie["fromrootvsys"] = "true"
        return mycookie
    else:
        print("Login Failed")
        return


def getAPI(host, uri):
    res = requests.get(url=host + "/" + uri, cookies=mycookie, verify=False)
    # print(res.json())
    return res.json()


def get_hostname_sn(HOST, username, password, port):
    fw = StoneHelper(ConnectionType.ssh, HOST, username, password, port)
    res = fw.send("show version")
    # print(res)
    time.sleep(1)
    fw.close()

    sn = re.search(r'\d{16}', res).group()
    # print(sn)
    hostname = re.search(r'(.+)#', res).group(1)
    # print(hostname)
    return {'SN': sn, 'HOSTNAME': hostname}


def save_to_db(devicename, sn, time):
    try:
        conn = pymysql.connect(host='10.85.222.2', user='root', passwd='hillstone', db='mysql', port=3306,
                               charset='utf8')
        cursor = conn.cursor()

        sql = "insert into devnet (devicename,sn,time) values ('%s','%s','%s')" % (devicename, sn, time)
        # print(sql)
        try:
            cursor.execute(sql)
            conn.commit()
            print("Insert to db successfully!")
        except:
            conn.rollback()

        cursor.execute('SELECT * FROM `devnet`')
        print(cursor.fetchall())

        cursor.close()
    except pymysql.Error as e:
        print(e)
    finally:
        conn.close()


def send_mail(devicename, sn, time):
    text = "Device name: %s; SN: %s; Time: %s;" % (devicename, sn, time)

    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header("发件人", 'utf-8')
    message['To'] = Header("收件人", "utf-8")
    message['Subject'] = Header('Mail from DevNet', 'utf-8')

    sender = '327105204@qq.com'
    receivers = ['327105204@qq.com']
    mail_host = "smtp.qq.com"
    mail_port = 25
    mail_user = "327105204"
    mail_pass = "password"
    try:
        smtpObj = smtplib.SMTP(mail_host, mail_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("Sent mail successfully")
    except smtplib.SMTPException:
        print("Sent mail failed")


if __name__ == '__main__':
    # disable https certificate warnings
    urllib3.disable_warnings()

    # define your firewall ip address
    host = "https://10.0.0.1:888"
    hostip = "10.0.0.1"
    sshport = 2233
    uri = 'rest/api/devicemonitor?query={"extraParams":{"monitorType":"status:cpu"}}'

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9999))

        msg = s.recv(1024).decode('utf-8')

        userpass = msg.split(',')
        username = userpass[0]
        password = userpass[1]

        s.close()

        # get cookie from function login()
        mycookie = login(host, username, password)
        cpu = getAPI(host, uri)
        oneminutecpu = cpu["result"][0]['1minute']
        print(oneminutecpu)

        cpu_alter_threshold = 50
        if float(oneminutecpu) > cpu_alter_threshold:
            dt = datetime.datetime.now()
            print(dt.isoformat())
            time.sleep(1)
            hostname_sn = get_hostname_sn(hostip, username, password, sshport)
            # print(hostname_sn["SN"], hostname_sn["HOSTNAME"])
            save_to_db(hostname_sn["HOSTNAME"], hostname_sn["SN"], dt.isoformat())
            send_mail(hostname_sn["HOSTNAME"], hostname_sn["SN"], dt.isoformat())
        time.sleep(5)
