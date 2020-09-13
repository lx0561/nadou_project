import datetime
import hashlib
import base64
import json
import requests # 使用该库可以发出http请求

class YunTongXin():
    base_url = "https://app.cloopen.com:8883"
    def __init__(self,accountSid,accountToken,appId,templateId):
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId


    # 1.构造url
    def get_request_url(self,sig):
        self.url = self.base_url+'/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s'%(self.accountSid,sig)
        return self.url

    # 2.生成时间戳
    def get_timestamp(self):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y%m%d%H%M%S')
        return now_str

    # 3.url的第三个参数sig
    def get_sig(self,timestamp):
        s = self.accountSid + self.accountToken + timestamp
        md5 = hashlib.md5()
        md5.update(s.encode())
        return md5.hexdigest().upper()

    # 4.构造请求头
    def get_request_header(self,timestamp):
        s = self.accountSid + ':' + timestamp
        b_s = base64.b64encode(s.encode()).decode()
        return {
            'Accept':'application/json',
            'Content-Type':'application/json;charset=utf-8',
            'Authorization':b_s
        }

    # 5.请求体
    def get_request_body(self,phone,code):
        data={
            'to':phone,
            'appId':self.appId,
            'templateId':self.templateId,
            'datas':[code,'3']
        }
        return data

    # 6.发送请求
    def do_request(self,url,header,body):
        res = requests.post(url,headers=header,data=json.dumps(body))
        return res.text

    # 7.完成短信发送
    def run(self,phone,code):
        timestamp = self.get_timestamp()
        sig = self.get_sig(timestamp)
        # 1.url
        url = self.get_request_url(sig)
        # 2.header
        header = self.get_request_header(timestamp)
        # 3.body
        body = self.get_request_body(phone,code)
        # 4.send request
        res = self.do_request(url,header,body)
        return res

if __name__ == '__main__':
    aid = '8a216da873cec1320174396157ba2794'
    atoken = '8803b27648824d98afea73ca244f699c'
    appid = '8a216da873cec132017439615893279a'
    tid = '1'
    x = YunTongXin(aid,atoken,appid,tid)
    res = x.run('13388175276','101010')
    print(res)