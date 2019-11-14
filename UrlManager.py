#!/usr/bin/env python
#-*- coding:utf-8 -*-

class UrlManager():
    def __init__(self):
        self.new_urls = []
        self.old_urls = []

    def get_url(self):
        '''
        获取未访问的url
        :return:
        '''
        url = self.new_urls.pop()
        if url not in self.old_urls:
            self.old_urls.insert(0, url)
        return url

    def add_url(self,url):
        '''
        添加url到未访问url列表中
        :param url: 要添加的url
        :return:
        '''
        if url not in self.old_urls and url not in self.new_urls:
            self.new_urls.insert(0, url)

    def add_urls(self,urls):
        '''
        添加url集合到url列表中
        :param urls: 要添加的url集合
        :return:
        '''
        for url in urls:
            self.add_url(url)

    def has_url(self):
        '''
        是否存在url,如存在则返回true，不存在返回false
        :return:
        '''
        if len(self.new_urls)!=0:
            return True
        return False
