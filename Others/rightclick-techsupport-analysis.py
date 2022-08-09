import re
import requests
from requests_toolbelt import MultipartEncoder
import sys
import webbrowser

url = 'http://10.88.16.40:8000/tacapp/techanl/'
sss = requests.Session()
res = sss.get(url=url)

# Try to get the csrfmiddlewaretoken from res.text
# result is a List if there are multiple matches.
reg = r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*)"'
pattern = re.compile(reg)
result = pattern.findall(res.text)
token = result[0]

#print(f"token is : {result}")

# Get Cookies from res.headers. Can use RE instead of split().
cookie = {}
cookie['csrftoken'] = res.headers['Set-Cookie'].split(';')[0].split('=')[1]
#print(f'cookie is {cookie}')

# Get file name from sys.argv.
filepath = sys.argv[1]
filename = filepath.split('\\')[-1]


#print(f"filename is {filename}")
#print(f"filepath is {filepath}")

# See enctype="multipart/form-data" in Chrome.
# The fields are found over wireshark captures, also see <input> label in the form in html.
m = MultipartEncoder(
    fields = {
        'csrfmiddlewaretoken':(None, token),
        'uploadfile':(filename, open(filepath, 'rb'), 'application/octet-stream'),
        'click': (None,'上传'),
    }
)

headers = {
    'Content-Type': m.content_type,
}
res = sss.post(url= url, data=m, cookies=cookie, headers=headers)


with open(r'tech-support-analysis-result.html', 'w+', encoding='utf-8') as f:
    f.write(res.text)

# open the result with default web browser.
webbrowser.open("tech-support-analysis-result.html")

