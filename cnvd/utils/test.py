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
startUrl = "https://www.cnvd.org.cn/flaw/show/CNVD-2019-18509"

def getResponse():
    """
    获取response
    :return:
    """
    response = requests.get(startUrl, headers=headers)

    return response


def getJslid(response):
    """
    :param response:
    :return:
    """
    cook = response.cookies
    return '; '.join(['='.join(item) for item in cook.items()])


def getClearance(response):
    """
    :return:
    """
    txt = ''.join(re.findall('<script>(.*?)</script>', response.text))
    func_return = txt.replace('eval', 'return')
    print(func_return)
    content = execjs.compile(func_return)
    eval_func = content.call('x')
    print(eval_func)

    name = re.findall(r'var (.*?)=function.*', eval_func)[0]
    print(name)

    mode_func = eval_func.replace('while(window._phantom||window.__phantomas){};', ''). \
        replace('document.cookie=', 'return').replace('if((function(){try{return !!window.addEventListener;}', ''). \
        replace("catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',%s,false)}" % name, ''). \
        replace("else{document.attachEvent('onreadystatechange',%s)}" % name, '').replace(
        r"setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);",
        '').replace('return return', 'return')
    print(mode_func)


    content = execjs.compile(mode_func)
    cookies = content.call(name)
    # print(cookies)
    clearance = cookies.split(';')[0]

    return clearance


def structureHeaders(cook, clearance):
    """
    构造新的headers
    :return:
    """

    cookie = {
        'cookie': cook + ';' + clearance
    }
    return dict(headers, **cookie)

if __name__ == "__main__":
    res = getResponse()
    cook = getJslid(res)
    print(cook)
    res = getClearance(res)
    res = structureHeaders(cook, res)
    print(res)
