#!/usr/bin/env python
#coding:utf-8
#Author:liangpeili

from bs4 import BeautifulSoup
import requests
import re
import spider_fang
import MySQLdb

def get_html(url):
    response = requests.get(url)
    html = response.content
    return html  #获取html内容 

def get_url(html):
    reg = r'href="(/chushou.+?\.htm)"'   # 正则表达式匹配
    urlre = re.compile(reg)
    urllist = re.findall(urlre, html)  # 查找所有匹配正则的链接并返回
    url_full = []
    for url1 in urllist:
        url_full.append("http://esf.fang.com"+url1)
    return list(set(url_full))

def get_sub_url(mainurl):
    response = requests.get(mainurl)  
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    main_url_list =re.findall(re.compile(r'url=(.*\.html)'), str(soup.head.contents[5]))
    if main_url_list:
        print main_url_list
        return main_url_list[0]   # 获取手机端的子链接
    else:
        return None

def insert_into_db(**kargs):
    print kargs
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="housebuyer",charset="utf8")
    cur = conn.cursor()
    cur.execute("insert into soufang (addr, title, price, room, area, zhname, district, comarea, phone, housedetail) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(kargs['addr'],kargs['title'], kargs['price'], kargs['room'], kargs['area'], kargs['zhname'], kargs['district'], kargs['comarea'], kargs['phone'], kargs['housedetail']))

if __name__ == "__main__":
    
    url = 'http://esf.fang.com/house/i34'
    for j in range(94,95):
        print j
        html = get_html('http://esf.fang.com/house/i3'+str(j))
        urllist = get_url(html)
   # print urllist
        suburllist=[]
        for mainurl in urllist:
            print mainurl
            suburllist.append(get_sub_url(mainurl))
            #print suburllist
        for i in suburllist:
            if i:
                html1 = spider_fang.get_html(i)
                spider_fang.get_content(html1)
            else:
                print 'no'
