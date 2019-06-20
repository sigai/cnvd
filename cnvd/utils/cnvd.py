from urllib.parse import urlencode
import re

import requests
from scrapy import Selector
import execjs  

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Cookie": "__jsluid=1225c87a7e36a7678ecce7d97cf04dab; __jsl_clearance=1560926407.27|0|3wbjpLt3X19kwxgRuhSb6slsolg%3D; JSESSIONID=716B4F8CEB8404805AD660EE1682E901",
    "DNT": "1",
    "Host": "www.cnvd.org.cn",
    "Origin": "https://www.cnvd.org.cn",
    "Referer": "https://www.cnvd.org.cn/flaw/typelist?typeId=29",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
url = "https://www.cnvd.org.cn/flaw/show/CNVD-2019-18509"

s = requests.Session()

parameters = {
    "typeId": 29,
    "max": 20,
    "offset": 0,
}
pattern = re.compile(r"<script>(.*)</script>")

def crawl(url="", parameters=None):
    try:
        res = s.get(url, headers=headers)
    except Exception as e:
        print(f"[-] Error.")
        print(e)
    else:
        print(res.status_code)
        print(res.headers)
        print(res.request.headers)
        with open("cookies.js", mode="wb") as f:
            f.write(res.content)
        js = pattern.findall(res.text)[0]
        js = js[4:]
        res = execjs.eval(js)
        print(res)

if __name__ == "__main__":
    crawl(url=url, parameters=parameters)
