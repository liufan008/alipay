import requests
from pyqrcode import QRCode
import re
import time,random
from io import BytesIO
from PIL import Image
import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
try:
    from httplib import BadStatusLine
except ImportError:
    from http.client import BadStatusLine
import logging


log=logging.getLogger('lChat')
class Login(object):
    def __init__(self):
        self.uid=''
        self.url=None
        self.host=''
        self.skey=''
        self.wxsid=''
        self.wxuin=''
        self.basturl=''
        self.request=requests.Session()
        self._13=str(int(time.time())*1000)
        self.DeviceID='e' + repr(random.random())[2:17]
        self.r=str(~int(time.time()))
        self.pass_ticket=''
        self.synckey=''
        self.syncurl=''
        self.User={}
        self.Synckey=[]
        self.timen=str(int(time.time()))
        self.headers ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        # 微信好友
        self.MemberCount=0
        self.MemberList={}
        # 微信消息
        self.AddMsgList={}
    def getuid(self):
        url='https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_='+str(int(time.time()))
        rsp=self.request.get(url)
        pat=r'window.QRLogin.code = (\d*); window.QRLogin.uuid = "([\s\S]*)";'
        uid=re.match(pat,rsp.text)
        if uid.group(1)=='200':
            self.uid=uid.group(2)
            print(self.uid)
            return True
        else:
            return False
#获取到需要扫描登录的二维码
    def get_qrc(self):
        url='https://login.weixin.qq.com/qrcode/'+self.uid
        rep=self.request.get(url)
        imqr=Image.open(BytesIO(rep.content))
        imqr.show()
#判断登录状态，一个uuid参数，上面获取过，一个时间戳，还有一个是r，抓包看了一下js，～new Date，对时间戳进行位运算
    def getLogin(self):
        url='https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid='+self.uid+'&tip=0&r='+str(~int(time.time()))+'&_='+str(int(time.time()))
        rep=self.request.get(url,).text
        pat=r'window.code=(\d*);'
        print(rep)
        paturl=r'window.redirect_uri="([\s\S]*)";'
        cod=re.match(pat,rep)
        if cod.group(1)=='200':
            back=re.search(paturl,rep)
            self.url=back.group(1)
            base=re.search(r'https://(.*?)/',back.group(1))
            self.basturl=base.group(1)
    def getLoginData(self):
        print(self.url)
        rep=self.request.get(self.url+'&fun=new&version=v2&lang=zh_CN').text
        return rep
    def getLogPar(self,data):
        self.skey=re.search(r'<skey>(.*?)</skey>',data).group(1)
        self.wxsid=re.search(r'<wxsid>(.*?)</wxsid>',data).group(1)
        self.pass_ticket=re.search(r'<pass_ticket>(.*?)</pass_ticket>',data).group(1)
        self.wxuin=re.search(r'<wxuin>(.*?)</wxuin>',data).group(1)
        print('**********************************************************************************************************')
        print('skey:%s',self.skey)
        print('wxsid:%s',self.wxsid)
        print('pass_ticket:%s',self.pass_ticket)
        print('wxuin:%s',self.wxuin)
        print('**********************************************************************************************************')
    def webxinit(self):
        url='https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r='+self.r+'&lang=zh_CN&pass_ticket='+self.pass_ticket
        postdata='{"BaseRequest":{"Uin":"'+self.wxuin+'","Sid":"'+self.wxsid+'","Skey":"'+self.skey+'","DeviceID":"'+self.DeviceID+'"}}'
        headers = {
            'ContentType': 'application/json; charset=UTF-8'}
        rep=requests.post(url,headers=headers,data=postdata).content.decode('utf-8','replace')
        back=json.loads(rep)
        self.User=back['User']
        self.Synckey=back['SyncKey']
        for i in back['SyncKey']['List']:
            self.synckey+=str(i['Key'])+'_'+str(i['Val'])+'|'
    def webwxstatusnotify(self):
        url='https://'+self.basturl+'/cgi-bin/mmwebwx-bin/webwxstatusnotify?lang=zh_CN&pass_ticket='+self.pass_ticket
        postdata='{"BaseRequest":{"Uin":'+self.wxuin+',"Sid":"'+self.wxsid+'","Skey":"'+self.skey+'","DeviceID":"'+self.DeviceID+'"},"Code":3,"FromUserName":"'+self.User['UserName']+'","ToUserName":"'+self.User['UserName']+'","ClientMsgId":'+self.timen+'}'
        rep=requests.post(url,postdata).content
    def testsynccheck(self):
        SyncHost = ['wx2.qq.com',
                'webpush.wx2.qq.com',
                'wx8.qq.com',
                'webpush.wx8.qq.com',
                'qq.com',
                'webpush.wx.qq.com',
                'web2.wechat.com',
                'webpush.web2.wechat.com',
                'wechat.com',
                'webpush.web.wechat.com',
                'webpush.weixin.qq.com',
                'webpush.wechat.com',
                'webpush1.wechat.com',
                'webpush2.wechat.com',
                'webpush.wx.qq.com',
                'webpush2.wx.qq.com']
        for host in SyncHost:
            self.syncurl = host
            [retcode,selector]=self.synccheck()
            if retcode=='0':
                break;
            else:
                print('没找到')
    def synccheck(self):
        url='https://'+self.syncurl+'/cgi-bin/mmwebwx-bin/synccheck'
        params = {
            'r': int(time.time()),
            'skey':self.skey,
            'sid':self.wxsid,
            'uin':self.wxuin,
            'deviceid':self.DeviceID,
            'synckey':self.synckey[:-1],
            '_':self.timen
        }
        try:
            rep=self.request.get(url,params=params,headers=self.headers,timeout=5).text
        except:
            rep=''
        par=r'window.synccheck={retcode:"(.*?)",selector:"(.*?)"}'
        if rep=='':
            return [0,-1]
        else:
            retcode=re.match(par,rep).group(1)
            selector=re.match(par,rep).group(2)
            return [retcode,selector]
    def webwxgetcontact(self):
        url='https://'+self.basturl+'/cgi-bin/mmwebwx-bin/webwxgetcontact'
        params={
            'lang':'zh_CN',
            'pass_ticket':'',
            'r':'',
            'seq':'',
            'skey':'',
        }
        rep=self.request.get(url,params=params,headers=self.headers,).content.decode('utf-8','replace')
        data=json.loads(rep)
        self.MemberCount=data['MemberCount']
        self.MemberList=data['MemberList']


    # def webwxbatchgetcontact(self):
    #     url='https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxbatchgetcontact?type=ex&r='+self.timen+'&lang=zh_CN&pass_ticket='+self.pass_ticket
    #     postdata='{"BaseRequest":{"Uin":'+self.wxuin+',"Sid":"'+self.wxsid+'","Skey":"'+self.skey+'","DeviceID":"'+self.DeviceID+'"},"Count":1,"List":[{"UserName":"'+self.User['UserName']+'","ChatRoomId":""}]}'
    #     rep=self.request.post(url,data=postdata,headers=self.headers).content.decode('utf-8','replace')
    #     print(rep)
    def webwxsync(self):
        url='https://'+self.basturl+'/cgi-bin/mmwebwx-bin/webwxsync?sid='+self.wxsid+'&skey='+self.skey+'&lang=zh_CN&pass_ticket='+self.pass_ticket
        postdata={
            'BaseRequest':'{"Uin":'+self.wxuin+',"Sid":"'+self.wxsid+'","Skey":"'+self.skey+'","DeviceID":"'+self.DeviceID+'"}',
            'SyncKey':self.Synckey,
            'rr':self.r
        }
        rep=self.request.post(url,data=json.dumps(postdata),headers=self.headers).content.decode('utf-8','replace')
        msg=json.loads(rep)
        self.AddMsgList=msg['AddMsgList']
        self.Synckey=msg['SyncKey']
        self.synckey=''
        for i in self.Synckey['List']:
            self.synckey+=str(i['Key'])+'_'+str(i['Val'])+'|'
        if  self.AddMsgList[0]['Content']!='':
            return True
        else:
            return False
    def sendMessage(self,FromUserName,ToUserName):
        url='https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg'
        params = {
            'BaseRequest': '{"Uin":'+self.wxuin+',"Sid":"'+self.wxsid+'","Skey":"'+self.skey+'","DeviceID":"'+self.DeviceID+'"}',
            'Msg': {
                "Type": 1,
                "Content":'123',
                "FromUserName": FromUserName,
                "ToUserName": ToUserName,
                "LocalID": self._13,
                "ClientMsgId": self._13
            }
        }
        print(FromUserName,ToUserName)
        postdata=json.dumps(params, ensure_ascii=False).encode('utf8')
        rep=self.request.post(url,data=postdata,headers=self.headers).content
        print(rep)

if __name__ == '__main__':
    a=Login()
    if a.getuid():
        a.get_qrc()
        while(a.url==None):
            a.getLogin()
            time.sleep(3)
        a.getLogPar(a.getLoginData())
        data=a.webxinit()
        a.webwxstatusnotify()
        a.webwxgetcontact()
        a.testsynccheck()
    while True:
            time.sleep(1)
            [retcode,selector]=a.synccheck()
            if int(selector)>0:
               if a.webwxsync():
                   print(a.AddMsgList[0]['FromUserName'],a.AddMsgList[0]['ToUserName'])





