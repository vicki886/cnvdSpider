import Spider
import argparse
import requests
import time
import datetime


def SpiderMain(currentTime, startTime, spider, page=5, level=2, type=1, method="time"):
    '''
    :param spider:
    :param page: 爬取的页面数量
    :param level: 当level为1时只返回高危漏洞,为2时返回高危、中危漏洞,为3时返回高、中、低漏洞
    :param type: 1:web应用漏洞,2:应用型漏洞,3:网络设备漏洞,4:操作系统漏洞
    :return:
    '''
    if type == 1:
        typestr = "29"
    elif type == 2:
        typestr = "28"
    elif type == 3:
        typestr = "31"
    else:
        typestr = "27"

    #获取
    if method == "time":
        spider.get_parse_urlsByTime(currentTime, startTime, type=typestr, level=level)
    elif method == "page":
        spider.get_parse_urls(page=page, type=typestr, level=level)
    else:
        print("unkown method,please select right method,as method=method or method=page")

    jsons = spider.get_parse_content(type)
    spider.write2doc(type, jsons)

    return spider


def main(currentTime,startTime,web,weblevel,app,applevel,device,devicelevel,sys,syslevel,method):
    start_time = time.time()
    print("程序运行中....")
    #新建一个爬虫对象
    spider = Spider.Spider()
    #web应用漏洞
    page = web
    level = weblevel
    type = 1
    spider = SpiderMain(currentTime,startTime,spider, page, level=level, type=type ,method=method)

    #应用程序漏洞
    page = app
    level = applevel
    type = 2
    spider = SpiderMain(currentTime,startTime,spider, page, level=level, type=type ,method=method)

    #网络设备漏洞
    page = device
    level = devicelevel
    type =3
    spider = SpiderMain(currentTime,startTime,spider, page, level=level ,type=type ,method=method)

    #操作系统漏洞
    page = sys
    level = syslevel
    type = 4
    spider = SpiderMain(currentTime,startTime,spider, page, level=level, type=type ,method=method)

    spider.save_doc(currentTime,startTime)
    end_time = time.time()
    print("总共花费了%s" % str((end_time-start_time)/60)+"分钟!")
#main()

argParser = argparse.ArgumentParser(prog="vickiTool v0.5", description="自动化生产安全通告")
argParser.add_argument("-w", "--web",default=0, help="请输入要爬取的web应用程序漏洞的页数", type=int)
argParser.add_argument("-wl", "--weblevel", default=2, help="请输入要爬取的web应用程序漏洞的爬取等级,默认等级为2", type=int, choices=[1, 2, 3])
argParser.add_argument("-a", "--app", default=0, help="请输入要爬取的应用程序漏洞的页数", type=int)
argParser.add_argument("-al", "--applevel", default=1, help="请输入要爬取的应用程序漏洞的爬取等级,默认等级为1", type=int, choices=[1, 2, 3])
argParser.add_argument("-d", "--device", default=0, help="请输入要爬取的应用程序漏洞的页数", type=int)
argParser.add_argument("-dl", "--devicelevel", default=1, help="请输入要爬取的网络设备漏洞的爬取等级,默认等级为1", type=int, choices=[1, 2, 3])
argParser.add_argument("-s", "--sys", default=0, help="请输入要爬取的应用程序漏洞的页数", type=int)
argParser.add_argument("-sl", "--syslevel", default=1, help="请输入要爬取的操作系统漏洞的爬取等级,默认等级为1", type=int, choices=[1, 2, 3])
argParser.add_argument("-m", "--method", default="time", help="请输入爬取的方法,默认按时间爬取7天的漏洞信息")
argParser.add_argument("-ST","--starttime",default=datetime.date.today()-datetime.timedelta(6), help="请输入开始日期", type=lambda s: datetime.date(*map(int, s.split('-'))))
argParser.add_argument("-ET","--endtime",default=datetime.date.today(), help="请输入结束日期", type=lambda s: datetime.date(*map(int, s.split('-'))))

args = argParser.parse_args()

web = args.web
weblevel = args.weblevel
app = args.app
applevel = args.applevel

device = args.device
devicelevel = args.devicelevel
sys = args.sys
syslevel = args.syslevel
#获取开始与结束日期strptime
startTime = args.starttime
endtime = args.endtime
method = args.method
#print(startTime)
if web == None or device==None or sys== None:
    print("缺少参数,-w,-d,-s参数是必须要的")
    exit(0)
main(endtime, startTime, web, weblevel, app, applevel, device, devicelevel, sys, syslevel, method=method)

