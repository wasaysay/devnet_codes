import requests
import base64
import json
import urllib3


def getbase64code(st):
    return str(base64.b64encode(st.encode("utf-8")), "utf-8")


def login(host, username, password):
    # After login success, return the cookies
    url = str(host) + "/rest/api/login"

    # need base64 encode username and password in newer versions
    base64_username = getbase64code(username)
    base64_password = getbase64code(password)

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
    print(res.json())
    return res.json()


if __name__ == '__main__':
    mycookie = login("https://10.0.0.1:888", "hillstone", "hillstone")

    uri = 'rest/api/policy_session_info?query={"fields":[],"conditions":[{"field":"flow0_srcip","operator":0,' \
          '"value":"10.0.0.190"},{"field":"flow0_srcip_mask","operator":0,"value":32}],"start":0,"limit":50,"page":1} '
    res = getAPI("https://10.0.0.1:888", uri)
    for item in res["result"]:
        print(item)
