'''
    py:自动信息采集
    author:amin
'''

import requests
import json
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def mail(answer, my_user):
    my_sender = '2101543615@qq.com'  # 发件人邮箱账号
    my_pass = 'emoxacplyrwdccaj'  # 发件人邮箱授权码，第一步得到的
    # my_user = '2089221335@qq.com'  # 收件人邮箱账号，可以发送给自己
    ret = True
    try:
        # msg=MIMEText('填写邮件内容','plain','utf-8')
        mail_msg = f"""
                        <p>{answer}</p>
                   """
        msg = MIMEText(mail_msg, 'html', 'utf-8')
        msg['From'] = formataddr(["托马斯提醒你", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([str(my_user), my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "自动信息采集"  # 邮件的主题，也可以说是标题
        '''
        QQ邮箱使用下面这种方式才成功
        '''
        # 发件人邮箱中的SMTP服务器，端口是25
        # server=smtplib.SMTP("smtp.qq.com", 25)
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465，固定的，不能更改 使用SSL模式
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.set_debuglevel(1)
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件信息
        server.quit()  # 关闭连接
    except Exception as err:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        # print(err)
        ret = False
    return ret


def user_Login_return_token(url,id):
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh - CN, zh;q = 0.9, en;q = 0.8, en - GB;q = 0.7, en - US;q = 0.6',
        'Connection': 'keep - alive',
        'Content - Length': '25',
        'Accept': 'application/json,text/plain,*/*',
        'Content-Type': 'application/json;harset=UTF-8',
        'isToken': 'false',
        'sec-ch-ua': "",
        'sec-ch-ua-mobile': '?1',
        'Sec-Fetch - Dest': 'empty',
        'Sec-Fetch - Mode': 'cors',
        'Sec-Fetch - Site': 'same-origin',
        'sec-ch-ua-platform'
        'User-Agent': 'Mozilla/5.0(iPhone;CPU iPhone OS 8_0 like MacOS X)AppleWebKit/600.1.4(KHTML,likeGecko) Mobile/12A365 MicroMessenger/5.4.1 NetType/WIFI Edg/101.0.4951.41'
    }
    data = {
        'username': id
    }
    # 将携带参数数据转换为json数据
    data = json.dumps(data)
    # 创建 session 对象
    session = requests.Session()
    # 使用 session 发送 post 请求获取 cookie
    tokens = session.post(url=url, headers=headers, data=data).text
    data_info = tokens[1:-1]
    data_info = re.findall('"token":\"(.*?)\"', data_info)
    # 获取到token值
    # print(data_info[0])
    return data_info[0]

def get_user_id(url,id,token):
    headers = {
        'sec-ch-ua': "",
        'sec-ch-ua-mobile': '?1',
        'Sec-Fetch - Dest': 'empty',
        'Sec-Fetch - Mode': 'cors',
        'Sec-Fetch - Site': 'same-origin',
        'sec-ch-ua-platform'
        'Content - Length': '25',
        'Connection': 'keep - alive',
        'Content-Type': 'application/json;harset=UTF-8',
        'Accept': 'application/json, text/plain,*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8, n-GB;q=0.7,en-US;q =0.6',
        'Authorization': 'Bearer ' + token,
        'User-Agent': 'Mozilla/5.0(iPhone;CPU iPhone OS 8_0 like MacOS X)AppleWebKit/600.1.4(KHTML,likeGecko) Mobile/12A365 MicroMessenger/5.4.1 NetType/WIFI Edg/101.0.4951.41'
    }
    cookies = {
        'username': id,
        'Admin-Token': token
    }
    userID = requests.get(url=url, headers=headers, cookies=cookies).text
    userID_info = re.findall('"userId":(.*?),', userID)
    # print(userID_info[0])
    # 返回用户的userID
    return userID_info[0]

def info_add(url, id, token, user_id, phone_num):
    headers = {
        'sec-ch-ua': "",
        'sec-ch-ua-mobile': '?1',
        'Sec-Fetch - Dest': 'empty',
        'Sec-Fetch - Mode': 'cors',
        'Sec-Fetch - Site': 'same-origin',
        'sec-ch-ua-platform'
        'Content - Length': '25',
        'Connection': 'keep - alive',
        'Content-Type': 'application/json;harset=UTF-8',
        'Accept': 'application/json, text/plain,*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8, n-GB;q=0.7,en-US;q =0.6',
        'Authorization': 'Bearer ' + token,
        'User-Agent': 'Mozilla/5.0(iPhone;CPU iPhone OS 8_0 like MacOS X)AppleWebKit/600.1.4(KHTML,likeGecko) Mobile/12A365 MicroMessenger/5.4.1 NetType/WIFI Edg/101.0.4951.41'
    }
    data = {
        # 次密接触
        'cmjc': '0',
        # 健康码状态
        'codeStatus': '0',
        'cqfk': '0',
        'current': '重庆市江津区圣泉街道重庆工程职业技术学院图书馆',
        'fhsjc': '',
        'fyDestination': '',
        'fyMsg': '',
        'fyfs': '',
        # 核酸检测
        'hsjc': '',
        'incq': '0',
        'inzgfx': '',
        # 健康管理
        'jkgl': '0',
        # 今日是否到（在）校
        'jrdx': '1',
        # 今日是否返渝
        'jrfy': '',
        # 今日是否离渝
        'jrly': '',
        'jzd': '',
        # 离校
        'lx': '0',
        # 离渝
        'lyDestination': '',
        'lyMsg': '',
        'lyfs': '',
        # 密切接触
        'mqjc': '0',
        'nativeCode': '',
        # 籍贯
        'nativePlace': '',
        'pc': '0',
        # 手机号
        'phone': phone_num,
        # 备注
        'remark': '',
        # 咳嗽腹泻症状
        'symptom': '0',
        # 体温是否正常
        'temperature': '0',
        # 体温信息
        'temperatureNumber': "",
        # 用户id
        'userId': user_id,
        # 疫苗接种情况
        'vaccine': '2',
        'zgfx': '0'
    }
    cookies = {
        'username': id,
        'Admin-Token': token
    }
    data = json.dumps(data)
    response = requests.post(url=url, headers=headers, data=data, cookies=cookies, verify=False).text
    # 打印填报状态
    # print(response)
    return re.findall('"msg":"(.*?)",',response)
def main():
    # 用户登陆界面
    url = 'https://sac.cqvie.edu.cn/server-health/userLogin'
    # 得到userID
    url_2 = 'https://sac.cqvie.edu.cn/server-health/getUserInfo'
    # 填报界面
    url_3 = 'https://sac.cqvie.edu.cn/server-health/epidemic/add'
    phone_nums = ['15223643819','18323303702']
    user_id = ['2033203041','2033203021']
    mail_user = ['2101543615@qq.com','1400918323@qq.com']
    try:
        for i in range(0,len(user_id)):
            # 获取到用户的cookie的token值
            tokens = user_Login_return_token(url,user_id[i])
            # 获取到用户的userID
            userID = get_user_id(url_2,user_id[i],tokens)
            # 信息填报
            tb_status = info_add(url_3,user_id[i],tokens,userID,phone_nums[i])
            print(tb_status)
            mail(tb_status,mail_user[i])
    except requests.exceptions.SSLError:
        print('请检查联网状态!')

# 程序开始
main()


# {"msg":"已提交完成","code":200,"data":{"epidemicId":"8037028ca05c4efd95d100dee11ce4d5","userId":"203707","phone":"15223643819","current":"重庆市江津区圣泉街道重庆工程职业技术学院图书馆","sfly":null,"incq":0,"codeStatus":0,"zgfx":0,"temperatureNumber":0.0,"temperature":0,"symptom":0,"bgszsq":null,"hsjc":null,"dqdqgl":null,"yfy":null,"inzgfx":null,"vaccine":2,"fhsjc":null,"pc":0,"jkgl":0,"jrdx":1,"lx":0,"remark":null}}