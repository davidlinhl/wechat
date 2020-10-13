# coding:utf-8
import itchat

# 登录
itchat.auto_login(hotReload=True)
# 获取所有群聊
# groups = itchat.get_chatrooms()
# 向一个群聊发文字
itchat.send(
    """<div class="bubble_cont primary ng-scope" ng-if="message.MsgType == CONF.MSGTYPE_APP &amp;&amp; message.AppMsgType == CONF.APPMSGTYPE_URL">
    <a ng-href="/cgi-bin/mmwebwx-bin/webwxcheckurl?requrl=http%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3ODEzMjg5Mg%3D%3D%26mid%3D2651713289%26idx%3D1%26sn%3Df42189f4e87f423cd622b91227e9c599%26chksm%3D84be2cfab3c9a5ecb6a28a7a3892ff72d885c8ded1e490f33efc4eb7216c20dc1f698dd8b11c%26mpshare%3D1%26scene%3D1%26srcid%3D1006SGkb87NnJkg54cIi5Gj8%26sharer_sharetime%3D1602001225191%26sharer_shareid%3D7a547340b861bc800d56ba7eaca4cde4%23rd&amp;skey=%40crypt_9f7cdc8_58394edc336a9610faca035a537c8f0a&amp;deviceid=e163617534228512&amp;pass_ticket=3HrnlEAiIaPa7RuRMs4cnws%252BBQfAqsQZg89ZA6P9ECU%253D&amp;opcode=2&amp;scene=1&amp;username=@de5f0813e7bd69b318a5f96f0e52872d068667bb38c69004a898c5c51ee52d85" ng-click="appMsgClick($event,message.MMAlert)" target="_blank" class="app" href="/cgi-bin/mmwebwx-bin/webwxcheckurl?requrl=http%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3ODEzMjg5Mg%3D%3D%26mid%3D2651713289%26idx%3D1%26sn%3Df42189f4e87f423cd622b91227e9c599%26chksm%3D84be2cfab3c9a5ecb6a28a7a3892ff72d885c8ded1e490f33efc4eb7216c20dc1f698dd8b11c%26mpshare%3D1%26scene%3D1%26srcid%3D1006SGkb87NnJkg54cIi5Gj8%26sharer_sharetime%3D1602001225191%26sharer_shareid%3D7a547340b861bc800d56ba7eaca4cde4%23rd&amp;skey=%40crypt_9f7cdc8_58394edc336a9610faca035a537c8f0a&amp;deviceid=e163617534228512&amp;pass_ticket=3HrnlEAiIaPa7RuRMs4cnws%252BBQfAqsQZg89ZA6P9ECU%253D&amp;opcode=2&amp;scene=1&amp;username=@de5f0813e7bd69b318a5f96f0e52872d068667bb38c69004a898c5c51ee52d85">
        <h4 class="title ng-binding" ng-bind="message.FileName">微醺酒上头，为何难跑出C位？</h4>
        <img class="cover" mm-src="/cgi-bin/mmwebwx-bin/webwxgetmsgimg?&amp;MsgID=1942713429626731632&amp;skey=%40crypt_9f7cdc8_58394edc336a9610faca035a537c8f0a&amp;type=slave" alt="" src="/cgi-bin/mmwebwx-bin/webwxgetmsgimg?&amp;MsgID=1942713429626731632&amp;skey=%40crypt_9f7cdc8_58394edc336a9610faca035a537c8f0a&amp;type=slave">
        <p class="desc ng-binding" ng-bind="message.MMAppMsgDesc">与高端白酒“社交货币”属性不同，微醺小酒熨帖的更多是情绪。</p>
    </a>
</div>
""",
    toUserName="filehelper",
)
# # 向一个群聊发图片
# itchat.send_image(
#     "/home/lin/Desktop/logo.jpg", toUserName="@@0dba5656c984d2cd970e1eaf7fabb5b58fcf3719b661d56115348675569b4a11"
# )


#
#
def get_friends():
    friends = itchat.get_friends()
    print(friends[0])
    for i in friends:
        # 获取个性签名
        signature = i["Signature"]
        print(signature)


#
#
# # 自动回复
# @itchat.msg_register(itchat.content.TEXT)
# def text_reply(msg):
#     return msg.text
#
#
# itchat.run()


if __name__ == "__main__":
    # get_friends()
    pass
