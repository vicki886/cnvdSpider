#!/usr/bin/env python
#-*- coding:utf-8 -*-

from writeDoc import doc
from docxtpl import DocxTemplate
import operator

import requests

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    print(proxy)
    while retry_count > 0:
        try:
            html = requests.get('http://ip111.cn/', proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html.text,html.status_code
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None


#html, code =getHtml()
#print(html, code)
s = {"data":{"a":123,"b":456}}
a = {"data":{"a":123,"b":56}}
#print(operator.eq(s,a))
s={}
def set():
    if any(s) == False:
        print("print")

if __name__ == '__main__':
    set()