import requests
import uuid
import random

"""
命名规则：
    第一次post请求：postA、postA_headers(请求头)、resp_postA(响应体)、、、、
    第二次get请求 ：getB、、、、
    第三次post请求：postC、、、、
"""

# 填入你的信息
username = "" # 填入登入账号
password = "" # 填入登录密码
mycontent = "" # 填入打卡数据

# 获取idToken
strings = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
deviceId = ''.join(random.sample(strings, 24))
clientId = uuid.uuid4().hex

postA_headers = {'Content-Length': '0', 'Host': 'token.huanghuai.edu.cn', 'Connection': 'Keep-Alive',
                 'Accept-Encoding': 'gzip', 'User-Agent': 'okhttp/3.12.1'
                 }
postA_datas = {'username': username, 'password': password, 'appId': 'com.lantu.MobileCampus.huanghuai', 'geo': '',
               'deviceId': deviceId, 'osType': 'android',
               'clientId': clientId
               }
resp_postA = requests.post("https://token.huanghuai.edu.cn/password/passwordLogin", data=postA_datas,
                           headers=postA_headers)
resp_dictA = resp_postA.json()  # 将返回的请求体转换为字典
resp_data = resp_dictA['data']
idToken = resp_data['idToken'] # 获取idToken值

# 获取cookie和token
getB_headers = {
    'Host': 'yq.huanghuai.edu.cn:7992',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 4LTE Build/PQ3A.190801.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.82 Mobile Safari/537.36 SuperApp',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'userToken': idToken,
    'X-Id-Token': idToken,
    'X-Requested-With': 'com.lantu.MobileCampus.huanghuai',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}
getB_cookies = {
    'userToken': idToken, 'Domain': '.huanghuai.edu.cn', 'Path': '/'
}
resp_getB = requests.get("https://yq.huanghuai.edu.cn:7992/cas/studentLogin", headers=getB_headers,
                         cookies=getB_cookies,
                         allow_redirects=False) # allow_redirects=False，禁止302自动跳转
p_cookie = resp_getB.headers["Set-Cookie"]
p_token = resp_getB.headers["Location"]
mytoken = p_token[p_token.find('token=') + 6:]  # 截取并获取token
mysession = p_cookie[p_cookie.find('SESSION=') + 8:p_cookie.find('; Path=/; Ht')]  # 截取并获取session

# 发送post请求、打卡
postC_headers = {
    'Host': 'yq.huanghuai.edu.cn:7992',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-auth-token': mytoken,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 4LTE Build/PQ3A.190801.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.82 Mobile Safari/537.36 SuperApp',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://yk.huanghuai.edu.cn:8993',
    'X-Requested-With': 'com.lantu.MobileCampus.huanghuai',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://yk.huanghuai.edu.cn:8993',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}
postC_cookies = {
    'userToken': idToken, 'Domain': '.huanghuai.edu.cn', 'Path': '/',
    'SESSION': mysession
}
postC_datas = {
    'content': mycontent
}
resp_postC = requests.post("https://yq.huanghuai.edu.cn:7992/questionAndAnser/wenjuanSubmit",
                           headers=postC_headers, cookies=postC_cookies, data=postC_datas)
resp_dictC = resp_postC.json()
success = resp_dictC['successful']  # 获取响应体的成功信息
message = resp_dictC['message']

# 发邮件模块
import smtplib
from email.mime.text import MIMEText

from_addr = ""  # 发送方邮箱
from_pwd = ""  # 发送方邮箱授权码
to_addr = ""  # 接收方的邮箱，接受打卡成功与否信息
smtp_srv = "smtp.qq.com"
if not (success):
    text = "自动打卡失败，请手动打卡并检查问题！[" + message + "]"
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = "打卡失败"
    msg['From'] = from_addr
    msg['To'] = to_addr

    try:
        srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)
        srv.login(from_addr, from_pwd)  # 使用授权码登录你的QQ邮箱
        srv.sendmail(from_addr, [to_addr], msg.as_string())  # 发送邮件
        print('发送成功-打卡失败')
    except Exception as e:
        print('发送失败-打卡失败')
    finally:
        srv.quit()  # 无论发送成功还是失败都要退出你的QQ邮箱
else:
    text = "已打卡！[" + message + "]"
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = "Successful"
    msg['From'] = from_addr
    msg['To'] = to_addr
    try:
        srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)
        srv.login(from_addr, from_pwd)
        srv.sendmail(from_addr, [to_addr], msg.as_string())
        print('发送成功-打卡成功')
    except Exception as e:
        print('发送失败-打卡成功')
    finally:
        srv.quit()
