import requests
import re
import MysqlUtil
import pymysql

class IosAppFree:

    def get_App_info(self,pag):
        url="https://itunes.apple.com/cn/genre/ios-%E5%B7%A5%E5%85%B7/id6002?mt=8&letter=*&page="+str(pag)+"#page"
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
                   }
        result=requests.get(url, headers=headers).text
        urls=re.findall(r'<li><a href="(.*?)">(.*?)</a> </li>',result)
        for i in urls:
            self.get_App_Data(i[0],i[1])
        return ""
    def get_App_Data(self,url,name):
        print(name)
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
                   }
        htmldata=requests.get(url, headers=headers).text
        p=re.compile(r'<li class="inline-list__item inline-list__item--bulleted">¥(.*?)</li>')
        ret=0
        for m in p.finditer(str(htmldata)):
            ret=m.group(1)
        if ret!=0:
            val=(url[url.rfind("/id")+3:url.rfind("?m")],name,ret,url,1)
             # val=
            self.insert(val)
            print('付费',name,'price',ret)
        else:
            print('free')
        return ''

    # 数据库操作
    def connect(self):
        db = pymysql.connect("localhost","root","326548","appDb")
        return db
    def insert(self,val):
        con=self.connect()
        cu=con.cursor()
        # sql='insert into appdata(appid,appname,appprice,appurl,appurl,state) VALUES (%s,%s,%s,%s,%s,%s)'
        sql='insert into appdata(appid,appname,appprice,appurl,state) VALUES (%s,%s,%s,%s,%s)'
        try:
            cu.execute(sql,val)
            con.commit()
        except:
            con.rollback()
            # 关闭数据库连接
        con.close()



if __name__ == '__main__':
    ios=IosAppFree()
    pag=1
    while pag<19:
        ios.get_App_info(pag)
        pag=pag+1
