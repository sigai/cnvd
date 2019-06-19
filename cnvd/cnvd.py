from urllib.parse import urlencode
import requests
from scrapy import Selector


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "__jsluid=1225c87a7e36a7678ecce7d97cf04dab; __jsl_clearance=1560926407.27|0|3wbjpLt3X19kwxgRuhSb6slsolg%3D; JSESSIONID=716B4F8CEB8404805AD660EE1682E901",
    "DNT": "1",
    "Host": "www.cnvd.org.cn",
    "Origin": "https://www.cnvd.org.cn",
    "Referer": "https://www.cnvd.org.cn/flaw/typelist?typeId=29",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
url = "https://www.cnvd.org.cn/flaw/typeResult?"


parameters = {
    "typeId": 29,
    "max": 20,
    "offset": 0,
}


def crawl(url="", parameters=None):
    if not url or not parameters:
        raise TypeError("[-]Stop.")
    try:
        res = requests.get(url+urlencode(parameters), headers=headers)
    except Exception as e:
        print(f"[-] Error.")
        print(e)
    else:
        response = Selector(text=res.text)
        rows = response.xpath('//table[@class="tlist"]/tbody/tr')
        


if __name__ == "__main__":
    for i in range(10):
        parameters["offset"] += parameters["max"]
        crawl(url=url, parameters=parameters)
        break