import requests
import  json
request=requests.Session();

def openRobot(state,user,text):
    message={}
    url='http://openapi.tuling123.com/openapi/api/v2'
    postdata={
        'reqType':0,
        'perception':'{"inputText":{"text": "你是谁"}}',
        'userInfo':'{"apiKey": "98eaefbd91f14666b658c48f3d4e67c1","userId": "DWASDAWDWADADASDAWDWAD"}'
    }
    postdata=json.dumps(postdata)
    print(postdata)
    rep=request.post(url,data=postdata).content.decode('utf-8','replace')
    resu=json.loads(rep)
    for i in resu['results']:
        print(i['values']['text'])
if __name__ == '__main__':
    openRobot(1,'asdfghjk','你好')
