import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime,timedelta
#运行时如果报错先在cmd里运行pip install requests
import requests
import subprocess
import json
import ctypes
import time

try:
    conf=open('biliconf.txt','r')
except:
    print('请先在目录下放入格式正确的biliconf.txt！按下回车退出')
    input()
    exit()
conf2=conf.read()
biliconf=json.loads(conf2)

version='v0.1'
#----------#
uid=biliconf.get('uid')
ctypes.windll.kernel32.SetConsoleTitleW('粉丝数监测 uid：'+str(uid))
url="https://api.bilibili.com/x/relation/stat?vmid="+uid
url2 = 'https://api.bilibili.com/x/space/acc/info?mid='+uid
fansold=0
delay=int(biliconf.get('delay'))  #刷新冷却 单位：秒
now = datetime.now()
#以下为日志文件保存名称，可自行更改
logsave=biliconf.get('logsave')
if logsave == "":
    logsave='log'+now.strftime("%Y%m%d-%H%M")+'.txt'

#发送和接收最好都使用QQ邮箱，且需要在手机上安装QQ邮箱客户端并登录接收用邮箱
mail_host=biliconf.get('mailhost')  #设置SMTP服务器，如使用QQ邮箱发送则无需更改
mail_user=biliconf.get('mailuser')  #用户名，即邮箱地址
mail_pass=biliconf.get('mailpass')  #密码，在网页端QQ邮箱启用smtp服务并将生成的授权码填入此处
sender = biliconf.get('sender')  #发送方，应和上面的邮箱地址相同
receivers = [biliconf.get('receiver')]  #接收邮件，可设置为你的QQ邮箱或者其他邮箱
#----------#

# 第三方 SMTP 服务，使用加密协议，下面的“粉丝变化通报”标题可自行修改
def send():
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header(biliconf.get('from'), 'utf-8')
    message['To'] =  Header(biliconf.get('to'), 'utf-8')
    subject = text
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = SMTP_SSL(mail_host)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
        return 0
    except smtplib.SMTPException:
        print ("错误：无法发送邮件")
        return 1

response = requests.get(url)
content = response.text
json_dict = json.loads(content)
jdata=json_dict['data']
fansold=jdata.get('follower')
response2 = requests.get(url2)
content2 = response2.text
json_dict2 = json.loads(content2)
jdata2=json_dict2['data']
name=jdata2.get('name')
now = datetime.now()
nowtime=now.strftime("%Y-%m-%d %H:%M:%S")
ctypes.windll.kernel32.SetConsoleTitleW('粉丝数实时监测 '+name+' uid：'+str(uid)+' 当前粉丝数：'+str(fansold))
print('粉丝数监测 '+version+' 网页版地址：https://shoyu.top/bili')
print('系统初始化，启动时间：'+nowtime+' UID：'+str(uid)+' 用户名：'+name+' 起始粉丝数：'+str(fansold))
print('监测日志将保存在：'+logsave)
print('===============开始监测===============')
print('刷新冷却已设置为：'+str(delay)+'秒')
logtxt = open(logsave,'w')
logtxt.write('粉丝数监测 '+version+' 网页版地址：https://shoyu.top/bili \n')
logtxt.write('系统初始化，启动时间：'+nowtime+' UID：'+str(uid)+' 用户名：'+name+' 起始粉丝数：'+str(fansold)+'\n')
logtxt.write('===============开始监测===============')
logtxt.write('\n')
logtxt.close()
while True:
    logtxt = open(logsave,'a')
    try:
        now = datetime.now()
        nowtime=now.strftime("%Y-%m-%d %H:%M:%S")
        #logtxt = open(logsave,'a')
        #logtxt.write('检测中...'+nowtime)
        #logtxt.write('\n')
        print('正在检测...',nowtime)
        response = requests.get(url)
        content = response.text
        json_dict = json.loads(content)
        jdata=json_dict['data']
        fans=jdata.get('follower')
        fansresult=fans-fansold
        if fansresult != 0:
            text=name+'的粉丝数变化量为 '+str(fansresult)+'，现在总共有粉丝 '+str(fans)
            print(text)
            now = datetime.now()
            nowtime=now.strftime("%Y-%m-%d %H:%M:%S")
            logtxt.write('[ '+nowtime+' ] '+text)
            logtxt.write('\n')
            ctypes.windll.kernel32.SetConsoleTitleW('粉丝数实时监测 '+name+' uid：'+str(uid)+' 当前粉丝数：'+str(fans))
            send()
        fansold=fans
    except:
        print('失败！')
        logtxt.write('[ '+nowtime+' ] '+'失败！')
        logtxt.write('\n')
    logtxt.close()
    time.sleep(delay)

