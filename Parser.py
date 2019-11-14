import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.parse
import urllib.request
import json
import datetime,time

def parse(url):
    '''
    返回html代码
    :param url:
    :return:
    '''

    try:
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"}
        text = requests.get(url, headers=headers, timeout=10)
        #print("当前的状态码为:%s " % text.status_code)
        code = text.status_code
        html = text.text
    except :
        code = 503
        html = ""
    return html,code


def get_urls(html, url, level=2):
    '''
    返回html中的cnvd漏洞url列表
    :param html:
    :param url:根url用来拼接新的url
    :param level: 当level为1时只返回高危漏洞,为2时返回高危、中危漏洞,为3时返回高、中、低漏洞
    :return:
    '''
    if  html == "":
        return []
    soup = BeautifulSoup(html, "lxml")
    list = soup.find_all('tr')
    urls = []

    for i in list:
        str = i.find_all('td')
        # level:漏洞等级
        security = str[1].contents[2].strip()
        joinurl = str[0].find('a')['href']
        fullurl = urljoin(url, joinurl)
        if level == 1:
            if security == '高':
                urls.append(fullurl)
        elif level == 2:
            if security == '高' or security == '中':
                urls.append(fullurl)
        else:
            urls.append(fullurl)
    return urls


def get_urlsByTime(currentTime,startTime,html, url, level=2):
    '''
    返回html中的cnvd漏洞url列表
    :param html:
    :param url:根url用来拼接新的url
    :param level: 当level为1时只返回高危漏洞,为2时返回高危、中危漏洞,为3时返回高、中、低漏洞
    :return:
    '''
    if  html == "":
        return []
    soup = BeautifulSoup(html, "lxml")
    list = soup.find_all('tr')
    urls = []
    flag = True
    for i in list:
        str = i.find_all('td')
        # level:漏洞等级
        security = str[1].contents[2].strip()
        joinurl = str[0].find('a')['href']
        fullurl = urljoin(url, joinurl)
        vulTime = str[5].text
        vulTime = datetime.date.fromisoformat(vulTime)
        #print("vultime:%s is in %s to %s " %(vulTime,startTime,currentTime))
        #判断漏洞发布日期
        if vulTime <= currentTime and vulTime>=startTime:
            #print(vulTime)
            if level == 1:
                if security == '高':
                    urls.append(fullurl)
            elif level == 2:
                if security == '高' or security == '中':
                    urls.append(fullurl)
            else:
                urls.append(fullurl)
        #当漏洞时间大于要爬取的结束时间时继续爬取下一页
        elif vulTime >currentTime:
            flag = True
        #当漏洞时间小于要爬取的开始时间时不爬取下一页
        elif vulTime<startTime:
            flag = False
    return urls, flag


def get_content(html):
    '''
    获取html中漏洞的具体信息
    :param html:
    :return: json数据
    '''
    try:
        if html == "":
            return ""
        data = {}
        soup = BeautifulSoup(html,"html.parser")
        table = soup.find("table",class_="gg_detail")
        title = soup.find("h1").text
        trs = table.find_all("tr")
        data['title']=title
        for idx, tr in enumerate(trs):
            tds = tr.find_all("td")
            key = tds[0].text.strip()
            value = clean_str(tds[1].text.strip())
            #print("key:%s,value:%s" %(key,value))
            data[key] = value
    except IndexError as e:
        pass
    except Exception as e:
       print("此漏洞写入word失败")
    return data


def clean_str(str1):
    str = str1.replace("\r", "")
    str = str.replace("\t", "")
    str = str.replace("\n", "")
    return str

def get_news_url(type=2):
    #国内新闻的地址
    baseurl = "https://www.easyaq.com/type/"+str(type)+".shtml"
    baseurl = "https://www.cnvd.org.cn/flaw/typelist?typeId=29"
    #解析获取国内新闻的url
    html,code = parse(baseurl)
    '''
    soup = BeautifulSoup(html,"html.parser")
    divs = soup.find("div", class_="listdeteal")
    h3 = soup.find("h3")
    joinurl = h3.find('a')['href']
    fullurl = urljoin(baseurl,joinurl)
    return fullurl
    '''
    return html






