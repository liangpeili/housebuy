#!/usr/bin/env python
#coding:utf-8
#Author:liangpeili

import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def query_db(district):
    conn = MySQLdb.connect(host="localhost",user="house",passwd="xxxxxx",db="housebuy",charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from soufang where district = %s limit 3", (district,))
    lines = cur.fetchall()
    i = 1

    return '标题:'+lines[0][2]+'\n'+'价格:'+lines[0][3]+'\n'+'户型:'+lines[0][4]+'\n'+'面积:'+lines[0][5]+'\n'+'中介:'+lines[0][6]+'\n'+'电话:'+lines[0][9]+'\n'+'地区:'+lines[0][7]+'\n'+'街道:'+lines[0][8]+'\n'+'详细介绍:'+lines[0][10]

if __name__ == "__main__":
    district = raw_input('你想买哪里的房子？')
    query_db(district)
