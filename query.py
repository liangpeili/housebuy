#!/usr/bin/env python
#coding:utf-8
#Author:liangpeili

import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def query_db(district):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="Ppnn13fish,",db="housebuy",charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from soufang where district = %s limit 3", (district,))
    lines = cur.fetchall()
    i = 1
#    for line in lines:
#        print "第%d条信息：" % i
#        print '标题:'+line[2]
#        print '价格:'+line[3]
#        print '户型:'+line[4]
#        print '面积:'+line[5]
#        print '中介:'+line[6]
#        print '电话:'+line[9]
#        print '地区:'+line[7]
#        print '街道:'+line[8]
#        print '详细介绍:'+line[10]
#        i += 1
#        print "-"* 30
    cur.close()
    conn.close()
    return '标题:'+lines[0][2]+'\n'+'价格:'+str(lines[0][3])+'\n'+'户型:'+lines[0][4]+'\n'+'面积:'+str(lines[0][5])+'\n'+'中介:'+lines[0][6]+'\n'+'电话:'+lines[0][9]+'\n'+'地区:'+lines[0][7]+'\n'+'街道:'+lines[0][8]+'\n'+'详细介绍:'+lines[0][10]

def query_db_area(area1, area2):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="Ppnn13fish,",db="housebuy",charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from soufang where area between %s and %s limit 3", (area1, area2))
    lines = cur.fetchall()
    
    cur.close()
    conn.close()
    return '标题:'+lines[0][2]+'\n'+'价格:'+str(lines[0][3])+'\n'+'户型:'+lines[0][4]+'\n'+'面积:'+str(lines[0][5])+'\n'+'中介:'+lines[0][6]+'\n'+'电话:'+lines[0][9]+'\n'+'地区:'+lines[0][7]+'\n'+'街道:'+lines[0][8]+'\n'+'详细介绍:'+lines[0][10]


def query_db_price(price1, price2):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="Ppnn13fish,",db="housebuy",charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from soufang where price between %s and %s limit 3", (price1, price2))
    lines = cur.fetchall()
    cur.close()
    conn.close()

    return '标题:'+lines[0][2]+'\n'+'价格:'+str(lines[0][3])+'\n'+'户型:'+lines[0][4]+'\n'+'面积:'+str(lines[0][5])+'\n'+'中介:'+lines[0][6]+'\n'+'电话:'+lines[0][9]+'\n'+'地区:'+lines[0][7]+'\n'+'街道:'+lines[0][8]+'\n'+'详细介绍:'+lines[0][10]

def query_db_all(price1, price2, area1, area2, addr):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="Ppnn13fish,",db="housebuy",charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from soufang where price between %s and %s and area between %s and %s and district = %s limit 3", (price1, price2, area1, area2, addr))
    lines = cur.fetchall()
    cur.close()
    conn.close()

    return '标题:'+lines[0][2]+'\n'+'价格:'+str(lines[0][3])+'\n'+'户型:'+lines[0][4]+'\n'+'面积:'+str(lines[0][5])+'\n'+'中介:'+lines[0][6]+'\n'+'电话:'+lines[0][9]+'\n'+'地区:'+lines[0][7]+'\n'+'街道:'+lines[0][8]+'\n'+'详细介绍:'+lines[0][10]

if __name__ == "__main__":
    district = raw_input('你想买哪里的房子？')
    query_db(district)

