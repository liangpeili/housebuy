#!/usr/bin/env python
#coding:utf-8

from flask import Flask,request
import hashlib
import xml.etree.ElementTree as ET
from query import query_db, query_db_price, query_db_area, query_db_all, query_db_cp, query_db_dp
import sys
import re


reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)


@app.route('/housebuytest')
def wechat_certificate():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    
    token = 'housebuytest'
    tmp_list = [token, timestamp, nonce]
    tmp_list.sort()
    tmp_str = "%s%s%s" % tuple(tmp_list)
    hash_str = hashlib.sha1(tmp_str).hexdigest()

    if hash_str == signature:
        return echostr
    else:
        return 'error'

@app.route('/housebuytest', methods=['POST'])
def return_district():
    mydic = {}
    data = request.data
    root = ET.fromstring(data)
    mydict = {child.tag:child.text for child in root}
    try:
        if mydict['Content'].lower() == 'hi':
            mydic['Content'] = '''你好，我是你的买房私人专家。
本微信号可以提供房源查询以及房价查询功能：
输入a+面积上下限根据面积筛选，例a50:100
输入p+价格上下限根据面积筛选，例p100:200
输入‘合并查询’将前几个条件合并查询
输入cp+地区名查询某地区房价均价，例cp中关村
输入dp+区县名查询某区县房价均价，例dp海淀
不加前缀，默认为区县名，例 海淀'''        
        elif re.match(r'^a', mydict['Content']):
            pattern_a = re.compile(r'\d+')
            global area
            area = pattern_a.findall(mydict['Content'])
            area1 = int(area[0])
            area2 = int(area[1])
            print "area1:" + str(area1) + "area2:" + str(area2)
            try:
                mydic['Content'] = query_db_area(area1, area2)
                print mydic['Content']
                
            except:
                print "query db erorr"
                mydic['Content'] = '数据库查询错误，请重新输入。'
                
        elif re.match(r'^p', mydict['Content']):
            pattern_p = re.compile(r'\d+')
            global price
            price = pattern_p.findall(mydict['Content'])
            price1 = int(price[0])
            price2 = int(price[1])
            print "price1:" + price[0] + "price2:" + price[1]
            try:
                mydic['Content'] = query_db_price(price1, price2)
                print mydic['Content']
                
            except:
                print "query db erorr"
                mydic['Content'] = '数据库查询错误，请重新输入。'
        elif re.match(r'^cp', mydict['Content']):
            xx=u"([\u4e00-\u9fa5]+)"
            pattern = re.compile(xx)
            temp = mydict['Content'].decode('utf8')
            comarea = pattern.findall(temp)
            
            try:
                mydic['Content'] = query_db_cp(comarea)
                print mydic['Content']
                
            except:
                print "query db erorr"
                mydic['Content'] = '数据库查询错误，请重新输入。'
        elif re.match(r'^dp', mydict['Content']):
            xx=u"([\u4e00-\u9fa5]+)"
            pattern = re.compile(xx)
            temp = mydict['Content'].decode('utf8')
            district = pattern.findall(temp)
            
            try:
                mydic['Content'] = query_db_dp(district)
                print mydic['Content']
                
            except:
                print "query db erorr"
                mydic['Content'] = '数据库查询错误，请重新输入。'
        else:
            print 'here else'
            if mydict['Content'] != '合并查询':
                global addr
                addr = mydict['Content']
                try:
                    mydic['Content'] = query_db(addr)
                    print mydic['Content']
                
                except:
                    print "query db erorr"
                    mydic['Content'] = '数据库查询错误，请重新输入。'
            elif mydict['Content'] == '合并查询':
                area1 = int(area[0])
                area2 = int(area[1])      
                price1 = int(price[0])
                price2 = int(price[1])
                print area[0] + area[1] + price[0] + price[1] + addr
                try:
                    mydic['Content'] = query_db_all(price1, price2, area1, area2, addr)
                    print mydic['Content']

                except:
                    print "query db erorr"
                    mydic['Content'] = '数据库查询错误，请重新输入。'

                #print 'here he'
                #print price, area, addr
            else:
                mydic['Content'] = '您的输入有误，请重新输入。'
    except:
        mydic['Content'] = '您的输入有误，请重新输入。'
    

    f = open('content.txt', 'a+')
    f.write(mydict['Content']+'\n')
    f.close()
    myxml = '''\
    <xml>
    <ToUserName><![CDATA[{}]]></ToUserName>
    <FromUserName><![CDATA[{}]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{}]]></Content></xml>
    '''.format(mydict['FromUserName'],mydict['ToUserName'],mydic['Content'])

    return myxml


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

