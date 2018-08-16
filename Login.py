import requests
from pyqrcode import QRCode
import re
import time
from io import BytesIO
from PIL import Image

class Login(object):
    def __init__(self):
        self.uid=None
#获取到一个重要的参数uuid，需要传一个时间戳的参数
    def getuid(self):
        url='https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_='+str(int(time.time()))
        rsp=requests.get(url)
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

        rep=requests.get(url)
        imqr=Image.open(BytesIO(rep.content))
        imqr.show()
#判断登录状态，一个uuid参数，上面获取过，一个时间戳，还有一个是r，抓包看了一下js，～new Date，对时间戳进行位运算
    def getLogin(self):
        url='https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid='+self.uid+'&tip=0&r='+str(~int(time.time()))+'&_='+str(int(time.time()))
        rep=requests.get(url)
        print(rep.text)
if __name__ == '__main__':
    a=Login()
    if a.getuid():
        a.get_qrc()
        b=1
        while(1<10):
            a.getLogin()
            time.sleep(3)
            b+=b

#登录已经实现了，扫码完成后会返回一个地址，打开直接就是登录状态...