#!/usr/bin/env python
#coding:utf-8
#Author:liangpeili

from bs4 import BeautifulSoup
import requests
import re
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def get_html(url):
 #   user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
 #   headers = {'User-Agent': user_agent,
 #              'content-type': 'application/json' }
 #   data = {'some': 'data'}
    response = requests.get(url)
    html = response.content
    return html   

def get_img(html):
    dst_dir = '/home/liangpeili/pic/'
    img_name = 1
    c = '.jpg'
    reg = r'src2="(.+?\.jpg)"'   # 正则表达式匹配
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)  # 查找所有匹配正则的链接并返回
    for img in imglist:
        img_content = requests.get(img)
        name = str(img_name)+c
        print img
        with open(dst_dir+name, "wb") as pic:
            print dst_dir+name
            pic.write(img_content.content)
#        urllib.urlretrieve(img, name)
        img_name += 1

def insert_into_db(**kargs):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="house_buyer",charset="utf8")
    cur = conn.cursor()
    cur.execute("insert into soufang (addr, title, price, room, area, zhname, district, comarea, phone, housedetail) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(kargs['addr'],kargs['title'], kargs['price'], kargs['room'], kargs['area'], kargs['zhname'], kargs['district'], kargs['comarea'], kargs['phone'], kargs['housedetail']))
    conn.commit()

def get_content(html):
    soup = BeautifulSoup(html, "lxml")
#    title = soup.title.text
#    print title.strip()
#    print soup.findall(id='addr')
    number = re.findall('[0-9]+', str(soup.find(attrs={"data-id":"phone"})))  #提取tag里的手机号
    housedetail = re.findall(re.compile(r'value="(.*)"'), str(soup.find(attrs={"data-id":"housedetail"}))) #提取tag里的详细内容
    if soup.find(id='addr'):
        addr = soup.find(id='addr').string
        title = soup.find(id='title').string
        price = soup.find(id='price').string
        room = soup.find(id='room').string
        area = soup.find(id='area').string
        zhname = soup.find(id='zhname').string
        district = soup.find(id='district').string
        comarea = soup.find(id='comarea').string
        number1 = number[0]
        housedetail1 = housedetail[0]
        print "地址",addr
        print "标题",title
        print "价格",price
        print "户型",room
        print "面积",area
        print "中介",zhname
        print "县区",district
        print "乡镇",comarea
        print "手机",number1
        print "详细描述",housedetail1
        insert_into_db(addr=addr, title=title, price=price, room=room, area=area, zhname=zhname, district=district, comarea=comarea, phone=number1, housedetail=housedetail1)

if __name__ == "__main__":
    
    url = 'http://m.fang.com/esf/bj/AGT_277306914.html'
    html = get_html(url)
    get_content(html)
#    get_img(html)
    

