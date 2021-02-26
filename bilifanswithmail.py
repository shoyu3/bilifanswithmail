import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime,timedelta
#运行时如果报错先在cmd里运行pip install requests
import requests
import os
import json
import time
import math

try:
    cook=open('cookie.txt','r')
except:
    print('请先在目录下放入格式正确的cookie.txt！按下回车退出')
    input()
    exit()
cookie=cook.read()

version='v0.3'
#----------#
uid=input('请输入UID：')
if uid == "":
    #UID初始值，填入自己的UID即可
    uid='229778960'
os.system('title 粉丝数实时监测 uid：'+str(uid))
url="https://api.bilibili.com/x/relation/stat?vmid="+uid
url2 = 'https://api.bilibili.com/x/space/acc/info?mid='+uid
fansold=0
delay=30  #刷新冷却 单位：秒
now = datetime.now()
#以下为日志文件保存名称，可自行更改
logsave='logs/log'+now.strftime("%Y%m%d-%H%M")+'.txt'

#发送和接收最好都使用QQ邮箱，且需要在手机上安装QQ邮箱客户端并登录接收用邮箱
mail_host="smtp.qq.com"  #设置SMTP服务器，如使用QQ邮箱发送则无需更改
mail_user="***@qq.com"  #用户名，即邮箱地址
mail_pass="ill***dchf"  #密码，在网页端QQ邮箱启用smtp服务并将生成的授权码填入此处
sender = '***@qq.com'  #发送方，应和上面的邮箱地址相同
receivers = ['***@qq.com']  #接收邮件，可设置为你的QQ邮箱或者其他邮箱
#----------#

# 第三方 SMTP 服务，使用加密协议，下面的“粉丝变化通报”标题可自行修改
def send():
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header("粉丝变化通报", 'utf-8')
    message['To'] =  Header("shoyu", 'utf-8')
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

def listurl(page):
    return 'https://api.bilibili.com/x/relation/followers?vmid='+str(uid)+'&pn='+str(page)

def gethtml(url, header):
    i = 0
    while i < 3:
        try:
            html = requests.get(url, headers=header, timeout=5)
            html.encoding = "utf-8"
            return html.text
        except requests.exceptions.RequestException:
            print('警告：超时'+str(i+1)+'次，位于'+str(errortime)+'页')
            i += 1

def checkwho(beginrun):
    global userlist_1
    global userlist_2
    global errortime
    print('尝试获取完整粉丝列表……')
    #print('cookie:'+cookie)
    header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
    "Accept":"*/*",
    "Sec-Fetch-Site":"none",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Dest":"empty",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cookie":cookie,
    }
    r=gethtml(listurl(1),header)
    errortime=1
    #r.encoding = "utf-8"
    #print(r.text)
    userlist_dict=json.loads(r)
    jdata=userlist_dict['data']
    jlist=jdata['list']
    totalfans=jdata.get('total')
    math2=math.ceil(jdata.get('total')/50)*50-totalfans
    pages=math.ceil(totalfans/50)
    #print(totalfans,pages,50-math2)
    #print('----------')
    times=1
    errortime=1
    userlist_1=[]
    while times < pages+1:
        #print('第'+str(times)+'页')
        #r=requests.get(listurl(times),headers=header)
        errortime=times
        r=gethtml(listurl(times), header)
        userlist_dict=json.loads(r)
        jdata=userlist_dict['data']
        jlist=jdata['list']
        times2=0
        if times != pages:
            while times2<50:
                #print(times2,jlist[times2].get('mid'))
                userlist_1.append(jlist[times2].get('mid'))
                times2=times2+1
        else:
            while times2<50-math2:
                #print(times2,jlist[times2].get('mid'))
                userlist_1.append(jlist[times2].get('mid'))
                times2=times2+1
        times=times+1
        time.sleep(0.3)
        #print('完成')
    userlist_1.sort()
    now = datetime.now()
    #以下为日志文件保存名称，可自行更改
    dirname='fanslist'
    listsave='/list'+now.strftime("%Y%m%d-%H%M")+'.txt'
    listtxt = open(dirname+listsave,'a')
    listtxt.write(str(userlist_1))
    listtxt.write('\n')
    listtxt.close()
    print('完成，共有 '+str(len(userlist_1))+' 位，已存至数组中，并保存为文件：'+dirname+listsave)
    if beginrun:
        print('第一次运行，跳过比对')
        userlist_2=userlist_1
        return 0
    else:
        #print(userlist_1)
        #print(userlist_2)
        if len(userlist_1)<len(userlist_2):
            theseare=set(userlist_2)-set(userlist_1)
        else:
            theseare=set(userlist_1)-set(userlist_2)
        userlist_2=userlist_1
        return theseare
    #print(userlist_1)

try:
    os.mkdir('fanslist')
except:
    print('fanslist目录已存在')
try:
    os.mkdir('logs')
except:
    print('logs目录已存在')
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
checkwho(True)
now = datetime.now()
nowtime=now.strftime("%Y-%m-%d %H:%M:%S")
os.system('title 粉丝数实时监测 '+name+' uid：'+str(uid)+' 当前粉丝数：'+str(fansold))
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
            try:
                thesewho=str(checkwho(False))
            except:
                thesewho='（获取出错）'
            #print(fansresult,fans,thesewho)
            text=name+'的粉丝数变化量为 '+str(fansresult)+'，现在总共有粉丝 '+str(fans)+'，变化源自这些用户：'+thesewho
            print(text)
            now = datetime.now()
            nowtime=now.strftime("%Y-%m-%d %H:%M:%S")
            logtxt.write('[ '+nowtime+' ] '+text)
            logtxt.write('\n')
            os.system('title 粉丝数实时监测 '+name+' uid：'+str(uid)+' 当前粉丝数：'+str(fans))
            send()
        fansold=fans
    except:
        print('失败！')
        logtxt.write('[ '+nowtime+' ] '+'失败！')
        logtxt.write('\n')
    logtxt.close()
    time.sleep(delay)

