import requests
from json import loads
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)
locate={
    '1':'44,44,',
    '2':'114,44,',
    '3':'185,44,',
    '4':'254,44,',
    '5':'44,124,',
    '6':'114,124,',
    '7':'185,124,',
    '8':'254,124,',
}
head={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
'Referer': 'https://kyfw.12306.cn/otn/login/init',
}
session=requests.Session()
session.verify=False
def login():
    resp1 = session.get(
    'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&',
    headers=head)
    with open('code.png','wb') as f:
        f.write(resp1.content)
    print('请输入验证码坐标代号：')
    code=input()
    write=code.split(',')
    codes=''
    for i in write:
        codes+=locate[i]
    data={
        'answer': codes,
        'login_site': 'E',
        'rand': 'sjrand'
    }
    resp=session.post('https://kyfw.12306.cn/passport/captcha/captcha-check',headers=head,data=data)
    html=loads(resp.content)
 
 
    if html['result_code']=='4':
        print('验证码校验成功！')
        login_url='https://kyfw.12306.cn/passport/web/login'
        user={
            'username': "*******",
            'password': "*******",
            'appid': 'otn'
        }
        resp2=session.post(login_url,headers=head,data=user)
        html=loads(resp2.content)
        print(resp2.text)
        if html['result_code'] == 0:
            print('登陆成功！')
        else:
            print('登陆失败！')
    else:
        print('验证码校验失败，正在重新请求页面...')
        login()
    pass
login()
