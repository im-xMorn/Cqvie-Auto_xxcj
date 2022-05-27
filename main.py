"""
    @py:自动信息采集
    @author:iCdo_X.
    @注：本脚本仅为个人提供技术经验！
"""
import requests
import json
import re
import urllib3
# 关闭请求警告报错
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def user_Login_return_token(url, id):
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN, zh;q = 0.9, en;q = 0.8, en - GB;q = 0.7, en - US;q = 0.6',
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
    # 将携带参数数据转换为 json 的 str 数据
    data = json.dumps(data)
    # 创建 session 对象，并获取 token 值
    session = requests.Session()
    tokens = session.post(url=url, headers=headers, data=data).text
    data_info = tokens[1:-1]
    data_info = re.findall('"token":\"(.*?)\"', data_info)
    # 获取到 token 值
    return data_info[0]


def get_user_id(url, id, token):
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
    # 返回用户的 userID
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
        # 是否在重庆 默认
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
        # 是否与排查信息有关联
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
    response = requests.post(url=url, headers=headers,
                             data=data, cookies=cookies, verify=False).text
    # 打印填报状态
    # print(response)
    return response


def main():
    # 用户登陆界面
    url = 'https://sac.cqvie.edu.cn/server-health/userLogin'
    # 得到 userID
    url_2 = 'https://sac.cqvie.edu.cn/server-health/getUserInfo'
    # 填报界面
    url_3 = 'https://sac.cqvie.edu.cn/server-health/epidemic/add'
    # 手机号
    phone_nums = ['15223643819', '13983167798', '18623303702',
                  '19112046641', '18725627599', '17781570443']
    # 学号
    user_id = ['2033203041', '2033203011', '2033203021',
               '2033203062', '2033203077', '2033203092']
    try:
        for i in range(0, len(user_id)):
            # 获取到用户的 cookie 的 token 值
            tokens = user_Login_return_token(url, user_id[i])
            # 获取到用户的 userID
            userID = get_user_id(url_2, user_id[i], tokens)
            # 信息填报
            tb_status = info_add(
                url_3, user_id[i], tokens, userID, phone_nums[i])
            # print(tb_status)
            tb_info = re.findall('"msg":"(.*?)",', tb_status)[0]
            # 返回填状态
            print(tb_info)
    except requests.exceptions.SSLError:
        print('请检查联网状态!')


# 程序开始
if __name__ == '__main__':
    main()
