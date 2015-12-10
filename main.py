#!/usr/bin/env python
#coding:utf-8
#Author:liangpeili


from flask import Flask,request
import hashlib
import xml.etree.ElementTree as ET
from query import query_db
import sys

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
        if mydict['Content'] == 'Hi':
            mydic['Content'] = '你好，我是你的买房私人专家。你想买哪里的房子？'
        else:
            mydic['Content'] = query_db(mydict['Content'])
    except:
        mydic['Content'] = '您的输入有误，请重新输入。'
    
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

