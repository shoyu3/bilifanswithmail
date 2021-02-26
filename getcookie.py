import requests
import json
import tkinter as tk
import qrcode
import os

url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
url2= 'http://passport.bilibili.com/qrcode/getLoginInfo'
#link = input('输入哔哩哔哩url')
#link = str(link)

# json 转get url得参数
def jsonDataToUrlParams(params_data):
    url_str = ''
    nums = 0
    max_nums = len(params_data)
    for key in params_data:
        nums = nums + 1
        # 如果是最后一位就不要带上&
        # 拼为url字符串
        if nums == max_nums:
            url_str += str(key) + '=' + str(params_data[key])
        else:            
            url_str += str(key) + '=' + str(params_data[key]) + ';'
    return url_str

print('获取扫码登录请求……')
response = requests.get(url)
content = response.text
json_dict = json.loads(content)
jdata=json_dict['data']
oauthlink=jdata.get('url')
oauthkey=jdata.get('oauthKey')
#oauthlink,
print('本次请求的oauthKey为：'+oauthkey)
print('使用B站客户端扫描弹出的二维码并确认登录后关闭该窗口')

qr = qrcode.QRCode(version=5,error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=8,border=4)
qr.add_data(oauthlink)
qr.make(fit=True)
img = qr.make_image()
img.save("qrcode.png")

master = tk.Tk()
master.title('使用B站客户端扫描并确认登录后关闭窗口')
master.resizable(0,0)
photo = tk.PhotoImage(file="qrcode.png")
w = tk.Label(master, image=photo)
w.pack()
master.mainloop()
os.unlink('qrcode.png')

#请求参数
data = {'oauthKey':oauthkey}
session = requests.session()
session.post(url2,data)
html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
cookie = jsonDataToUrlParams(html_set_cookie)
#print(html_set_cookie)
print('获取到的cookie如下：'+cookie)
print('尝试使用获取到的cookie进行模拟登录……')
header={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
"Cookie":cookie,
}
r=requests.get('http://api.bilibili.com/x/space/myinfo',headers=header).text
userinfo_dict=json.loads(r)
try:
    jdata=userinfo_dict['data']
    uid=jdata.get('mid')
    name=jdata.get('name')
    level=jdata.get('level')
    coins=jdata.get('coins')
    print('模拟登录成功，UID：'+str(uid)+'，用户名：'+name+'，等级 '+str(level)+'，拥有 '+str(coins)+' 枚硬币')
    outtxt = open('cookie.txt','w')
    outtxt.write(cookie)
    outtxt.close()
    input('已将cookie写入同一目录下的cookie.txt！按下回车退出')
except:
    input('模拟登录失败！可能是二维码过期或未进行登录，按下回车退出')

