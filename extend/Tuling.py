import requests
import  json
request=requests.Session();

def openRobot(state=1,user='dawdawdwa',text='你好我是机器人'):
    url='http://openapi.tuling123.com/openapi/api/v2'
    postdata={
        'reqType':0,
        'perception':'{"inputText":{"text":"'+text+'"}}',
        'userInfo':'{"apiKey": "98eaefbd91f14666b658c48f3d4e67c1","userId": "'+user+'"}'
    }
    postdata=json.dumps(postdata)
    try:
        rep=request.post(url,data=postdata).content.decode('utf-8','replace')
        resu=json.loads(rep)
        resu=resu['results']
        return resu
    except Exception as e:
        pass
