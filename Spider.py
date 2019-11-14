import requests
from Parser import *
import UrlManager
import random
from writeDoc import doc
import time



class Spider(object):
    def __init__(self):
        self.urlManager = UrlManager.UrlManager()
        self.doc = doc()

    def get_parse_urls(self, page=5, type=29 ,level=2):
        '''
        获取类型解析的所有url
        :param page:
        :param
        :return:
        '''
        #获取所有要解析的url
        for i in range(page):
            tmp = i*20
            url = "https://www.cnvd.org.cn/flaw/typeResult?typeId="+type+"&max=20&offset=%s" %tmp
            html,code = parse(url)
            retry_count = 6
            while code != 200 and retry_count > 0:
                second = random.randint(20, 30)
                print("被防火墙拦截延迟%ss,网页状态码为%s" % (second, str(code)))
                time.sleep(second)
                html, code = parse(url)
                retry_count -= 1
            urls = get_urls(html, url, level=level)
            print(url+" has %s" % len(urls))
            self.urlManager.add_urls(urls)

    def get_parse_urlsByTime(self,currentTime,startTime, type=29 ,level=2):
        '''
        获取类型解析的所有url
        :param page:
        :param
        :return:
        '''
        flag = True
        i=0
        max = 100
        #获取所有要解析的url
        while flag:
            tmp = i*max
            url = "https://www.cnvd.org.cn/flaw/typeResult?typeId="+type+"&max="+str(max)+"&offset=%s" %tmp
            html,code = parse(url)
            retry_count = 6
            while code != 200 and retry_count > 0:
                second = random.randint(20, 30)
                print("被防火墙拦截延迟%ss,网页状态码为%s" % (second, str(code)))
                time.sleep(second)
                html, code = parse(url)
                retry_count -= 1
            urls,flag = get_urlsByTime(currentTime,startTime,html, url, level=level)
            print(url+" has %s" % len(urls))
            self.urlManager.add_urls(urls)
            i +=1

    def get_parse_content(self, type):
        '''
        返回存入各类漏洞信息的json数据
        :return:jsons
        '''
        data_list = []
        i = 0
        while self.urlManager.has_url():
            url = self.urlManager.get_url()
            html,code = parse(url)
            retry_count = 6
            while code != 200 and retry_count > 0:
                second = random.randint(20, 30)
                print("被防火墙拦截延迟%ss,网页状态码为%s." % (second, str(code)))
                time.sleep(second)
                html, code = parse(url)
                retry_count -= 1
            data = get_content(html)
            if  data == None:
                print("%s 未读取到数据..." % url)
                continue
            print("type"+str(type)+": num("+str(i)+")"+url+"正在存入json数据.....")
            #print(data)
            sleeptime = random.randint(1, 3)
            time.sleep(sleeptime)
            #print("sleep %ss time" % sleeptime)
            data_list.append(data)
            i += 1
        return data_list

    def write2doc(self, type, data_list):
        self.doc.add_table(data_list, type=type)
        print("%s type success to write to doc！" % type)

    def save_doc(self,current_time, start_time):
        self.doc.save_doc(current_time, start_time)




