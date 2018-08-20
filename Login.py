import requests
from pyqrcode import QRCode
import re
import time,random
from io import BytesIO
from PIL import Image
import json

try:
    from httplib import BadStatusLine
except ImportError:
    from http.client import BadStatusLine
import logging

from extend import Tuling
logging.basicConfig(level=logging.INFO,format=('%(asctime)s:''%(message)s'),datefmt='%Y-%m-%d')  #
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
        self.DeviceID='e' + repr(random.random())[2:17]
        self.r=str(~int(time.time()))
        self.pass_ticket=''
        self.synckey=''
        self.syncurl=''
        self.Synckey=[]
        self. _13 = str(int(time.time() * 1000)) + \
                            str(random.random())[:5].replace('.', '')
        self.timen=str(int(time.time()))
        self.headers ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        #自己的信息
        self.User={}
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
            return True
        else:
            return False
    def get_qrc(self):
        url='https://login.weixin.qq.com/qrcode/'+self.uid
        rep=self.request.get(url)
        imqr=Image.open(BytesIO(rep.content))
        imqr.show()
    def getLogin(self):
        url='https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid='+self.uid+'&tip=0&r='+str(~int(time.time()))+'&_='+str(int(time.time()))
        rep=self.request.get(url,).text
        pat=r'window.code=(\d*);'
        paturl=r'window.redirect_uri="([\s\S]*)";'
        cod=re.match(pat,rep)
        if cod.group(1)=='200':
            back=re.search(paturl,rep)
            self.url=back.group(1)
            base=re.search(r'https://(.*?)/',back.group(1))
            self.basturl=base.group(1)
    def getLoginData(self):
        rep=self.request.get(self.url+'&fun=new&version=v2&lang=zh_CN').text
        return rep
    def getLogPar(self,data):
        self.skey=re.search(r'<skey>(.*?)</skey>',data).group(1)
        self.wxsid=re.search(r'<wxsid>(.*?)</wxsid>',data).group(1)
        self.pass_ticket=re.search(r'<pass_ticket>(.*?)</pass_ticket>',data).group(1)
        self.wxuin=re.search(r'<wxuin>(.*?)</wxuin>',data).group(1)
        print('*'*66)
        print('skey:%s',self.skey)
        print('wxsid:%s',self.wxsid)
        print('pass_ticket:%s',self.pass_ticket)
        print('wxuin:%s',self.wxuin)
        print('*'*66)
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
                pass
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
    def sendMessage(self,FromUserName,ToUserName,msg='哈哈'):

        url='https://'+self.basturl+'/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket='+self.pass_ticket
        self. _13 = str(int(time.time() * 1000)) + \
                    str(random.random())[:5].replace('.', '')
        params = {
            'BaseRequest': '{"Uin":'+self.wxuin+',"Sid":"'+self.wxsid+'","Skey":"'+self.skey+'","DeviceID":"'+self.DeviceID+'"}',
            'Msg': {
                "Type": 1,
                "Content":msg,
                "FromUserName": FromUserName,
                "ToUserName": ToUserName,
                "LocalID": self._13,
                "ClientMsgId": self._13
            },
            'Scene':0
        }
        postdata=json.dumps(params, ensure_ascii=False).encode('utf8')
        rep=self.request.post(url,data=postdata,headers=self.headers).content
    def messageManger(self):
        for it in self.AddMsgList:
            if it['MsgType']==1:
                print('收到一条新消息------------->',it['Content'])
                for item in Tuling.openRobot(1,it['FromUserName'][1:-33],it['Content']):
                    self.sendMessage(it['ToUserName'],it['FromUserName'],item['values']['text'])
                    logging.info('机器人自动回复------------>{0}'.format(item['values']['text']))
                    time.sleep(2)
    def start(self):
                logging.info("网页微信启动中");
                self.getuid()
                self.get_qrc()
                logging.info("扫描二维码登录");
                while(self.url==None):
                        self.getLogin()
                        time.sleep(3)
                self.getLogPar(self.getLoginData())
                logging.info("登录成功，初始化中");
                self.webxinit()
                logging.info("初始化成功，开启消息通知");
                self.webwxstatusnotify()
                logging.info("获取联系人信息");
                self.webwxgetcontact()
                logging.info("获取服务器地址");
                self.testsynccheck()
                logging.info("开始消息监听");
                while True:
                    [retcode,selector]=self.synccheck()
                    if int(selector)>0:
                        self.webwxsync()
                        self.messageManger()


if __name__ == '__main__':
    w=Login()
    w.start()
