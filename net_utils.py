#! python
# coding=UTF-8
from requests import session
from user_agent import generate_user_agent



def headers():
    header = {
        'User-Agent': generate_user_agent(device_type='desktop', os=('mac', 'linux', 'win', 'android'))
    }
    return header

# 读取网络资源
def fetch_source(url):

    s = session()
    resp = s.get(url, headers=headers())
    resp.encoding = resp.apparent_encoding
    if resp.status_code == 200:
        return resp.text
    else:
        fetch_source(url)



def get(url):
    response = get(url, headers=headers(), timeout=6)
    return response.content