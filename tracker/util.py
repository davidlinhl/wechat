"""
1. 统计所有群的成员数量
2. 和上次的成员列表对比,获取新进群人数和退群人数
"""

import os
import time
import datetime
import pickle

import itchat


itchat.auto_login(hotReload=True)


# 获取所有群聊

"""
groupid和userid 只在一次登录过程中是一致的,所以所有记录都是按照群名来保存的,群名不要改,而且最好不要包含特殊表情
"""


def get_group_names():
    """获取群总数.
    注意群需要保存到联系人才能看见

    Returns
    -------
    int
        当前共加入了多少个群.

    """
    # TODO: 好像推出了的群仍然会统计,可能需要时间生效?
    # NOTE: 注意删除之后的群仍然会统计,不要随便删群
    # TODO: 添加一个ignore列表,忽略这些群,弥补退群之后仍然能看到成员
    groups = itchat.get_chatrooms()
    names = [g["NickName"] for g in groups if len(g["NickName"]) != 0]
    return names


# print(get_group_names())


def get_mbr_list(group_name, save=True):
    """获取一个群里所有的成员,并添加pkl记录.

    Parametersrm
    ----------

    group_id : str
        这个群的名字.

    Returns
    -------
    list
        群里所有人的id和昵称.

    """
    group_id = group_name
    if group_name[0] != "@":
        group_id = itchat.search_chatrooms(name=group_name)[0]["UserName"]
    group = itchat.update_chatroom(group_id)
    mbrs = []
    for mbr in group["MemberList"]:
        mbrs.append(mbr["NickName"])

    if not save:
        return mbrs

    mbr_file_name = os.path.join("member", group_name + ".mbrlist")
    if not os.path.exists(mbr_file_name):
        with open(mbr_file_name, "wb") as f:
            mbr_record = {int(time.time()): mbrs}
            pickle.dump(mbr_record, f)
    else:
        with open(mbr_file_name, "rb") as f:
            mbr_record = pickle.load(f)
        mbr_record[int(time.time())] = mbrs
        with open(mbr_file_name, "wb") as f:
            pickle.dump(mbr_record, f)
    return mbrs


# print(get_mbr_list("test"))


def get_mbr_lists():
    """获取账户下所有群的成员,并pkl保存.

    Returns
    -------
    dict
        群名:所有成员.

    """
    all_mbrs = {}
    groups = get_group_names()
    for n in groups:
        mbrs = get_mbr_list(n)
        all_mbrs[n] = mbrs
    with open("all_mbr/" + str(int(time.time())) + ".pkl", "wb") as f:
        pickle.dump(all_mbrs, f)
    return all_mbrs


# print(get_mbr_lists())


def get_group_mbrs():
    mbr_lists = get_mbr_lists()
    mbrs = []
    for l in mbr_lists.values():
        for name in l:
            mbrs.append(name)
    return mbrs


# print(get_group_mbrs())


def get_unique_group_mbrs():
    mbrs = get_group_mbrs()
    unique = []
    for name in mbrs:
        if name not in unique:
            unique.append(name)
    return unique


# print(get_unique_group_mbrs())


def get_yesterday_mbr(group_name):
    """获取一个群昨天的成员.
    找昨天最后的一条记录

    Parameters
    ----------
    group_name : str
        群名称.

    Returns
    -------
    list
        昨天的群成员昵称列表.

    """
    today0_ts = int(time.mktime(datetime.date.today().timetuple()))
    mbr_file_name = os.path.join("member", group_name + ".mbrlist")
    with open(mbr_file_name, "rb") as f:
        mbr_records = pickle.load(f)

    max_ts = 0
    yesterday_mbr = []
    for k, v in mbr_records.items():
        if k < today0_ts and k > today0_ts - 86400:
            if k > max_ts:
                max_ts = k
                yesterday_mbr = mbr_records[k]
    return yesterday_mbr


# print(get_yesterday_mbr("test"))


def diff_mbr(old_mbr, new_mbr):
    leave_num = 0
    for id in old_mbr:
        if id not in new_mbr:
            leave_num += 1
    join_num = 0
    for id in new_mbr:
        if id not in old_mbr:
            join_num += 1
    return len(new_mbr), join_num, leave_num


# old_mbr = [
#     ["@4755983ebdb7af788383e8ec89f2499de992c14da93973da4e25163231fbaef4", "多语言代码生成器"],
#     ["@0ba8590199ea60aadd0151eb854de9689fc036f997d963e46134a5154d847113", "运营小喇叭63"],
#     ["@84418264aa79e181a1b2d25142a6f0fc", "艾琳(｡･ω･｡)ﾉ♡"],
#     ["@1", "test"],
# ]
# new_mbr = [
#     ["@4755983ebdb7af788383e8ec89f2499de992c14da93973da4e25163231fbaef4", "多语言代码生成器"],
#     ["@0ba8590199ea60aadd0151eb854de9689fc036f997d963e46134a5154d847113", "运营小喇叭63"],
#     ["@84418264aa79e181a1b2d25142a6f0fc", "艾琳(｡･ω･｡)ﾉ♡"],
#     ["@2", "new"],
# ]
#
# print(diff_mbr(old_mbr, new_mbr))


def cal_join_leave():
    """计算今天所有群进群和退群的人数.

    Returns
    -------
    dict
        今天所有群的人数,进群人数,退群人数.

    """
    mbr_lists = get_mbr_lists()
    diffs = {}
    for name, mbr in mbr_lists.items():
        yesterday_mbr = get_yesterday_mbr(name)
        diffs[name] = diff_mbr(yesterday_mbr, mbr)
    return diffs


# print(cal_join_leave())
