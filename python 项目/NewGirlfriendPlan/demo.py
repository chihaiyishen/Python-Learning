from __future__ import unicode_literals
import requests
import itchat
import time

def get_news():
    url = "http://open.iciba.com/dsapi"
    r = requests.get(url)
    contents = r.json()['content']
    translation = r.json()['translation']
    return contents, translation

def send_news():
    try:
        # 登陆你的微信账号，会弹出网页二维码，扫描即可
        itchat.auto_login(hotReload=True)
        # 获取你对应的好友备注，这里的小明我只是举个例子
        # 改成你最心爱的人的名字。
        my_friend = itchat.search_friends(name=u'小明')
        # 获取对应名称的一串数字
        XiaoMing = my_friend[0]["UserName"]
        # 获取金山字典的内容
        message1 = str(get_news()[0])
        content = str(get_news()[1][17:])
        message2 = str(content)
        message3 = "来自你最爱的人"
        # 发送消息
        itchat.send(message1, toUserName=XiaoMing)
        itchat.send(message2, toUserName=XiaoMing)
        itchat.send(message3, toUserName=XiaoMing)
        # 每86400秒（1天），发送1次，
        # 不用linux的定时任务是因为每次登陆都需要扫描二维码登陆，
        # 很麻烦的一件事，就让他一直挂着吧
        # t = time(86400, send_news())
        # t.start()
    except:
        message4 = u"今天最爱你的人出现了 bug /(ㄒoㄒ)/~~"
        itchat.send(message4, toUserName=XiaoMing)

def main():
    send_news()

if __name__ == '__main__':
    main()