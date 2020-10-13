from util import Clicker

clicker = Clicker()
while True:
    print("输入操作名称")
    cmd = input()
    if cmd == "currpos":
        # clicker.get_mouse()
        pass
    elif cmd == "getgroups":
        clicker.get_groups()
    elif cmd == "getlayout":
        clicker.get_layout()
    elif cmd == "savelayout":
        clicker.save_layout()
    elif cmd == "readlayout":
        clicker.save_layout()
    elif cmd == "bulksend":
        clicker.bulk_send()
    elif cmd == "exit":
        exit()
    else:
        print("不支持的操作")
    print("---------")
