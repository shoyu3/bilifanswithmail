# 哔哩哔哩粉丝数监测&邮件通知

其实就是一个十分简单的python程序，一百行多一点的代码，Releases里有已经编译和打包过的文件（网页版地址[https://shoyu.top/bili](https://shoyu.top/bili)）

觉得下载慢的可以前往码云（[点击这里](https://gitee.com/shoyu3/bilifanswithmail)）或蓝奏云（[点击这里，密码0000](https://io3.lanzous.com/b0dwltk8j)）下载

### 用法

#### 电脑上没有安装Python且操作系统为64位：

下载Releases里的```bilifanswithmailv0.3-win-x64.zip```并解压，把解压后的目录里的```biliconf.txt.example```改名为```biliconf.txt```并按需修改其中的参数，然后运行```run.bat```即可

参数参考如下（不要直接从这里复制！）：
```
{
    "uid":"229778960",    想要监测的UID，一般填写自己的
    "delay":"30",    刷新延时，单位是秒，默认30，刷新太快可能会被封接口
    "logsave":"",    日志保存文件名，默认为空，程序会自动以“log+日期+时间”的格式命名
    "mailhost":"smtp.qq.com",    SMTP服务器，使用QQ邮箱发件的无需修改，其他服务商需要按照对应的设定进行修改
    "mailuser":"10000@qq.com",    用来发件的邮箱的用户名，一般和邮箱地址相同
    "mailpass":"abcdef",    用来发件的邮箱的密码或授权码，QQ邮箱需要到mail.qq.com下登录并生成授权码，然后填入
    "sender":"10000@qq.com",    发件地址，一般和邮件地址相同
    "receiver":"10001@qq.com",    收件地址，填写用来接收通知邮件的邮箱地址
    "from":"粉丝变化通报",    发件方，可作为邮件标题（手机上通知会以此为标题）
    "to":"shoyu"    收件方，目前无效果，可随意填
}
```

#### 电脑上已经安装Python或操作系统为32位（假定已经安装Python）：

下载仓库根目录的```bilifanswithmail.py```并修改里面的参数比如smtp用户名密码以及收件邮箱等，然后在命令行窗口运行即可

**如果上面的没有看明白的话按第一条走就行了**

### 更新日志
v0.3（2021-2-19）

添加变化用户监测（比对粉丝列表，1000粉以下处理一次大约需要十几秒）

v0.2（跳过）

v0.1（2021-2-16）

初版
