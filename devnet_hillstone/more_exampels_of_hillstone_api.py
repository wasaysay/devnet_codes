import requests
import base64
import json
import urllib3


def getBase64code(st):
    return (str(base64.b64encode(st.encode("utf-8")), "utf-8"))


def login(host):
    # After login success, return the cookies
    url = str(host) + "/rest/api/login"

    # Change the username and password accordingly

    username = "hillstone"
    password = "hillstone"

    # need base64 encode username and password in newer versions
    base64_username = getBase64code(username)
    base64_password = getBase64code(password)

    # login data
    body = {"lang": "zh_CN", 'userName': base64_username, 'password': base64_password}

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
    print(res.json())
    return res.json()


def postAPI(host, uri, body):
    res = requests.post(url=host + "/" + uri, cookies=mycookie, data=json.dumps(body), verify=False)
    print(res.json())
    return res.json()


if __name__ == '__main__':
    # disable https certificate warnings
    urllib3.disable_warnings()

    # define your firewall ip address
    host = "https://10.0.0.1:888"

    # get cookie from function login()
    mycookie = login(host)

    # Below is the example to get device time
    # set URI according to the function you need (can be found in restapi document)
    uri = "rest/api/devicetime"
    getAPI(host, uri)

    # Below is the example to get polices
    uri = "rest/api/policy"
    getAPI(host, uri)

    # Below is the example to create address book
    uri = "rest/api/addrbook"
    # Change the body fields accordingly
    body = {
        "name": "testadd391",
        "ip": [{
            "ip_addr": "27.4.4.4",
            "netmask": "24",
            "flag": 0
        }
        ],
        "range": [{
            "min": "25.3.3.3",
            "max": "25.3.3.9",
            "flag": 0
        }
        ],
        "host": [{
            "dns_name": "2589"
        }
        ],
        "wildcard": [{
            "ip_addr": "27.4.4.4",
            "netmask": "255.255.255.214"
        }
        ]
    }

    postAPI(host, uri, body)

    # Gget address book

    uri = "rest/api/addrbook"
    getAPI(host, uri)


    # Get App Group details
    uri = 'rest/traffic?query={"fields":[],"conditions":[],"sorts":[],"lifeTime":{"interval":"realtime"},' \
          '"extraParams":{"monitorType":"rank:appgroup","withTotal":true,"orderBy":"totalStream","keyword":""},' \
          '"start":0,"limit":50,"page":1} '
    getAPI(host, uri)

    # Get App  details
    print("Get APP details")
    uri = 'rest/traffic?query={"fields":[],"conditions":[],"sorts":[],"lifeTime":{"interval":"realtime"},' \
          '"extraParams":{"monitorType":"rank:app","withTotal":true,"withUserNum":true,"orderBy":"totalStream","keyword":""},' \
          '"start":0,"limit":50,"page":1} '
    getAPI(host, uri)

    # Get User Monitor>Address Book Details
    print("Get User Monitor>Address Book Details")
    uri = 'rest/traffic?query={"fields":[],"conditions":[],"sorts":[],"lifeTime":{"interval":"hour"},"extraParams":{' \
          '"monitorType":"rank:usergroup","withTotal":true,"orderBy":"totalStream","keyword":""},"start":0,' \
          '"limit":50,"page":1} '
    getAPI(host, uri)


