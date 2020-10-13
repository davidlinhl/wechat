"""
1. 统计所有群的成员数量
2. 和上次的成员列表对比,获取新进群人数和退群人数
"""
import itchat


itchat.auto_login(hotReload=True)
# 获取所有群聊


def get_mbr_list(group_name):
    """获取一个群里所有的成员.

    Parametersrm
    ----------
    group_name : str
        这个群的群名.

    Returns
    -------
    list
        群里所有人的id和昵称.

    """
    group = itchat.search_chatrooms(name=group_name)
    # print(group)
    group = itchat.update_chatroom(group[0]["UserName"])
    mbrs = []
    for mbr in group["MemberList"]:
        mbrs.append([mbr["UserName"], mbr["NickName"]])
    return mbrs


def get_all_mbrs():
    """获取账户下所有群的成员,并pkl保存.

    Returns
    -------
    dict
        群名:所有成员.

    """
    all_mbrs = {}
    groups = itchat.get_chatrooms()
    for g in groups:
        # print(g)
        mbrs = get_mbr_list(g["NickName"])
        all_mbrs[g["NickName"]] = mbrs
    with open("all_mbrs.pkl", "wb") as f:
        pickle.dump(all_mbrs, f)
    return all_mbrs


print(get_all_mbrs())
