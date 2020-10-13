import time
import os
import pickle

import itchat
import pyautogui
import pyperclip


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, rhs):
        x = self.x - rhs.x
        y = self.y - rhs.y
        return Point(x, y)


class Clicker:
    def __init__(self):
        self.poses = {}
        self.poses["base_pos"] = Point(535, 235)
        # filehelper里一个文章的位置，点右键能出菜单都可以，窗口不要太靠边
        self.poses["article_pos"] = Point(1150, 600)
        # 分享文章的位置，点击右键之后分享那一行的位置
        self.poses["share_article_pos"] = Point(1200, 640)
        # 搜索要分享到的群的搜索框位置
        self.poses["share_search_pos"] = Point(800, 330)
        # 选择完点击发送的位置
        self.poses["send_button_pos"] = Point(1100, 750)
        # 首页搜索联系人的搜索框
        self.poses["contact_search_pos"] = Point(680, 260)
        # 第一个搜索结果的位置
        self.poses["first_hit_pos"] = Point(700, 360)

    def open_file_transfer(self):
        time.sleep(1)
        self.click(self.poses["contact_search_pos"])
        pyperclip.copy("File")
        pyautogui.hotkey("ctrl", "v")
        time.sleep(3)
        pyautogui.press("enter")

    def save_layout(self):
        # pyautogui.move(self.poses["send_button_pos"].x, self.poses["send_button_pos"].y)
        filename = input("请输入保存布局生成的文件名: ")
        with open(os.path.join("layout", filename + ".pkl"), "wb") as f:
            pickle.dump(self.poses, f)
        f.close()

    def read_layout(self):
        names = os.listdir("layout")
        for idx, name in enumerate(names):
            print(idx, ": ", name)
        idx = input("请输入要读取布局前面的编号： ")
        with open(os.path.join("layout", names[int(idx)]), "rb") as f:
            self.poses = pickle.load(f)
        f.close()

    def get_mouse(self):
        x, y = pyautogui.position()
        return Point(x, y)

    def click(self, p, button="left"):
        pyautogui.click(p.x, p.y, button=button)

    def get_layout(self):
        """获取用户微信布局."""
        pyautogui.alert(
            """Start to get ur wechat layout, sorry but the gui only supports english, check the code for chinese details.\n
            Press enter to continue when finish each step.
            """
        )
        # 打开微信软件，不要让其他任何软件遮挡它
        pyautogui.alert("Now open the wechat desktop app and make it float at the top")

        # 将鼠标放到微信窗口的左上角
        pyautogui.alert(
            "Now put ur mouse at the upper left corner of the window, be accurate!! Or all clicks will not be accurate"
        )
        self.poses["base_pos"] = self.get_mouse()

        # 将鼠标放到左上角搜索输入框里
        pyautogui.alert("Now put ur mouse into the top left search input box")
        self.poses["contact_search_pos"] = self.get_mouse()
        time.sleep(2)
        self.click(self.poses["contact_search_pos"])

        # 将鼠标放到第一个搜索结果的位置
        pyautogui.alert("Now put ur mouse into the first search result")
        self.poses["first_hit_pos"] = self.get_mouse()
        pyautogui.press("esc")

        time.sleep(1)
        self.open_file_transfer()

        # 向文件传输发送一条链接消息，把鼠标放到这条消息里面，这里注意这个消息不要太靠近右下角，否则右键点击之后位置就不知道是哪了
        pyautogui.alert(
            "Now share a link message to ur file trasfer and put ur mouse into the message\n Then put ur mouse in the middle of the forward line"
        )
        self.poses["article_pos"] = self.get_mouse()
        self.click(self.poses["article_pos"], "right")

        # 将鼠标放到转发那一行的中间
        # pyautogui.alert("Now put ur mouse in the middle of the forward line")
        time.sleep(3)
        self.poses["share_article_pos"] = self.get_mouse()
        self.click(self.poses["share_article_pos"])

        # 将鼠标放到转发的那个搜索框里面
        pyautogui.alert("Now put ur mouse in the search box for contacts to send to")
        self.poses["share_search_pos"] = self.get_mouse()

        # 将鼠标放到搜索的第一个结果里面
        pyautogui.alert("Now put ur mouse in the first search result")
        self.poses["first_hit_pos"] = self.get_mouse()

        # 将鼠标放到右下角绿色的发送按钮里
        pyautogui.alert("Now put ur mouse in the lower right send button")
        self.poses["send_button_pos"] = self.get_mouse()

        # 最后推出到主界面
        pyautogui.alert(
            "Be aware that all the functionalities need to start from the main interface, so now go back to the main interface "
        )
        print("页面布局采集完成, savelayout 操作可以保存")

    def calibrate_base(self):
        # 打开微信软件，不要让其他任何软件遮挡它
        pyautogui.alert("Now open the wechat desktop app and make it float at the top")

        # 将鼠标放到微信窗口的左上角
        pyautogui.alert(
            "Now put ur mouse at the upper left corner of the window, be accurate!! Or all clicks will not be accurate"
        )
        base = self.get_mouse()

    def share_send(self, to_contact):
        time.sleep(3)
        # 右键点击文章
        self.click(self.poses["article_pos"], "right")
        time.sleep(2)
        # 点击forward
        self.click(self.poses["share_article_pos"])
        time.sleep(1)
        # 点击分享搜索框
        self.click(self.poses["share_search_pos"])
        # 将群名复制进去
        pyperclip.copy(to_contact)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")

        res = pyautogui.confirm(
            text="Click Ok to send, Click Cancel to skip this", title="Confirm send?", buttons=["OK", "Cancel"]
        )
        if res == "OK":
            time.sleep(1)
            self.click(self.poses["send_button_pos"])
        else:
            print("Cancel send")
            time.sleep(0.5)
            self.click(self.poses["share_search_pos"])
            time.sleep(0.5)
            pyautogui.press("esc")

    def send_message(self, to_contact, message):
        time.sleep(3)
        self.click(self.poses["contact_search_pos"])
        time.sleep(1)
        pyperclip.copy(to_contact)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("enter")

        time.sleep(1)
        pyperclip.copy(message)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        res = pyautogui.confirm(
            text="Click Ok to send, Click Cancel to skip this", title="Confirm send?", buttons=["OK", "Cancel"]
        )
        if res == "OK":
            self.click(self.poses["send_button_pos"])
            pyautogui.press("enter")
        else:
            print("cancel send")

    def bulk_send(self):
        names = os.listdir("contact")
        for idx, name in enumerate(names):
            print(idx, ": ", name)
        idx = input("输入你想要发送的联系人列表序号，将对这个列表中所有的联系人进行链接消息转发: ")
        with open(os.path.join("contact", names[int(idx)]), "r") as f:
            contacts = f.readlines()
        contacts = [n[:-1] for n in contacts]
        print("---------")
        for n in contacts:
            print(n)
        print("---------")
        cmd = input("即将批量发送到以上联系人，按 Y/y 确认， 其他任意键取消:  ")
        if cmd != "y" and cmd != "Y":
            return
        cmd = input("即将发送，请将需要发送的链接消息先发送到File Helper，并且保证其是最后一条消息。完成后按任意键回车继续:  ")

        pyautogui.alert(
            "About to start bulk sending, plz make sure wechat is displayed in the front and is at the main interface"
        )
        for n in contacts:
            self.open_file_transfer()
            self.share_send(n)
            self.send_message(n, "message content")
        print("批量发送完成")

    def get_groups(self):
        """获取所有群聊的名称和基本信息.
        注意：群聊必须保存到通讯录才能被读取出来
        """
        print("获取群组信息")
        itchat.auto_login(hotReload=True)
        # 获取所有群聊
        groups = itchat.get_chatrooms()
        with open(os.path.join("contact", "all_groups.txt"), "w") as f:
            for gcontact_search_pos in groups:
                print(g["NickName"], file=f)
                # print(g["MemberCount"], end=",", file=f)
                # print(file=f)

    # def get_mouse(slef):
    #     print("两秒后获取当前鼠标位置")
    #     time.sleep(2)
    #     print(pyautogui.position())
