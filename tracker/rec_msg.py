import itchat
from itchat.content import *
from influxdb import InfluxDBClient

"""
text 文本
map 位置
card 名片
note 通知
sharing 分享
picture 图片
recording 录音
attachment 文件
video 视频
friends 好友
"""

client = InfluxDBClient("localhost", 8086, "root", "root", "wechat")

"""
{
    'MsgId': '3963924623040390871',
    'FromUserName': '@cd2fa9bc5f6538511e66a3b577821a3c4c8fcb72e849807c94bc2bc97c1aa361',
    'ToUserName': '@@90b4cb8f031b28b47366c728329c891dfc81839c94811eb2c203d0d665e74924',
    'MsgType': 1,
    'Content': 'k',
    'Status': 3,
    'ImgStatus': 1,
    'CreateTime': 1603214604,
    'VoiceLength': 0,
    'PlayLength': 0,
    'FileName': '',
    'FileSize': '',
    'MediaId': '',
    'Url': '',
    'AppMsgType': 0,
    'StatusNotifyCode': 0,
    'StatusNotifyUserName': '',
    'RecommendInfo': {'UserName': '', 'NickName': '', 'QQNum': 0, 'Province': '', 'City': '', 'Content': '', 'Signature': '', 'Alias': '', 'Scene': 0, 'VerifyFlag': 0, 'AttrStatus': 0, 'Sex': 0, 'Ticket': '', 'OpCode': 0},
    'ForwardFlag': 0,
    'AppInfo': {'AppID': '', 'Type': 0},
    'HasProductId': 0,
    'Ticket': '',
    'ImgHeight': 0,
    'ImgWidth': 0,
    'SubMsgType': 0,
    'NewMsgId': 3963924623040390871,
    'OriContent': '',
    'EncryFileName': '',
    'ActualNickName': '多语言代码生成器',
    'IsAt': False,
    'ActualUserName': '@cd2fa9bc5f6538511e66a3b577821a3c4c8fcb72e849807c94bc2bc97c1aa361',
    'User':
    <Chatroom: {
        'MemberList':
        <ContactList: [
            <ChatroomMember: {
                'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@cd2fa9bc5f6538511e66a3b577821a3c4c8fcb72e849807c94bc2bc97c1aa361', 'NickName': '多语言代码生成器', 'AttrStatus': 33788773, 'PYInitial': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': ''
            }>,
            <ChatroomMember: {
                'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@f58081e90773533b8d0dc66079cff1da7b31cd718db72ce993ec9600b75c9e3a', 'NickName': '运营小喇叭63', 'AttrStatus': 135207, 'PYInitial': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': ''
            }>
        ]>,
        'UserName': '@@90b4cb8f031b28b47366c728329c891dfc81839c94811eb2c203d0d665e74924',
        'NickName': 'silent',
        'Sex': 0,
        'HeadImgUpdateFlag': 1,
        'ContactType': 0,
        'Alias': '',
        'ChatRoomOwner': '@cd2fa9bc5f6538511e66a3b577821a3c4c8fcb72e849807c94bc2bc97c1aa361',
        'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=0&username=@@90b4cb8f031b28b47366c728329c891dfc81839c94811eb2c203d0d665e74924&skey=@crypt_9f7cdc8_b26b209e2678019dd4df0856bd3e5959',
        'ContactFlag': 2051,
        'MemberCount': 2,
        'HideInputBarFlag': 0,
        'Signature': '',
        'VerifyFlag': 0,
        'RemarkName': '',
        'Statues': 1,
        'AttrStatus': 0,
        'Province': '',
        'City': '',
        'SnsFlag': 0,
        'KeyWord': '',
        'OwnerUin': 0,
        'IsAdmin': None,
        'Self':
            <ChatroomMember:{
                'MemberList': <ContactList: []>,
                'Uin': 0,
                'UserName': '@cd2fa9bc5f6538511e66a3b577821a3c4c8fcb72e849807c94bc2bc97c1aa361',
                'NickName': '多语言代码生成器',
                'AttrStatus': 33788773,
                'PYInitial': '',
                'PYQuanPin': '',
                'RemarkPYInitial': '',
                'RemarkPYQuanPin': '',
                'MemberStatus': 0,
                'DisplayName': '',
                'KeyWord': ''
            }>
        }>,
    'Type': 'Text',
    'Text': 'k'
}

"""

"""群里有多少人,群人数的曲线,群发言热度的曲线,退群和加群的曲线"""
"""显示一个人加了多少个群,在群里说了多少话,发消息的热度曲线"""
"""主页显示有多少个群,群里总共有多少人,去重之后有多少人,发消息热度的折线图,今天有多少人进群,有多少人退群"""

"""
群：
    群总数
    加群统计（研究是不是能收到加群消息，精确看加群时间） 总数和每个群
    退群统计（定时任务，每隔一段时间统计） 总数和每个群

人：
    人总数
    所有一个人发的消息
    时间粒度发言条数

消息：
    消息总数
"""
# 处理私聊文字消息
@itchat.msg_register([TEXT], isFriendChat=True)
def do_checks(msg):
    sender = msg["User"]["UserName"]
    rcver = msg["ToUserName"]
    print(sender, rcver)
    if sender == "filehelper" and rcver == "filehelper":
        print("run")
        itchat.send(u"[BOT]: Starting to run analysys", "filehelper")


# 处理群聊文字消息
@itchat.msg_register([TEXT], isGroupChat=True)
def rec_text(msg):
    group_name = msg["User"]["NickName"]
    sender = msg["ActualNickName"]
    content = msg["Content"]
    print(group_name, sender, content)
    json_body = [
        {
            "measurement": "message",
            "tags": {"group": group_name, "sender": sender, "type": "text"},
            "fields": {"text": content, "group_m": group_name, "sender_m": sender},
        }
    ]
    client.write_points(json_body)


@itchat.msg_register([MAP], isGroupChat=True)
def rec_map(msg):
    print(msg)


@itchat.msg_register([CARD], isGroupChat=True, isFriendChat=True, isMpChat=True)
def rec_card(msg):
    print(msg)


@itchat.msg_register([NOTE], isGroupChat=True, isFriendChat=True, isMpChat=True)
def rec_note(msg):
    print(msg)


@itchat.msg_register([SHARING], isGroupChat=True, isFriendChat=True, isMpChat=True)
def rec_sharing(msg):
    print(msg)


@itchat.msg_register([PICTURE], isGroupChat=True, isFriendChat=True, isMpChat=True)
def rec_pic(msg):
    print(msg)


@itchat.msg_register([RECORDING], isGroupChat=True, isFriendChat=True, isMpChat=True)
def rec_rec(msg):
    print(msg)


@itchat.msg_register([ATTACHMENT], isGroupChat=True, isFriendChat=True, isMpChat=True)
def rec_file(msg):
    print(msg)


@itchat.msg_register([VIDEO], isGroupChat=True, isFriendChat=True, isMpChat=True)
def rec_video(msg):
    print(msg)


@itchat.msg_register(FRIENDS, isGroupChat=True, isFriendChat=True, isMpChat=True)
def rec_friend_req(msg):
    print(msg)


itchat.auto_login(hotReload=True, enableCmdQR=2)
print("Logged in")
itchat.run()
