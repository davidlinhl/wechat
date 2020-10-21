# coding=utf-8
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options
import pickle
import json
from influxdb import InfluxDBClient
import itertools


# import util


influx_client = InfluxDBClient("zjp.zdcd.online", 8086, "root", "root", "wechat")

define("port", default=1122, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # join_leaves = util.cal_join_leave()
        # joins = leaves = 0
        # for r in join_leaves.values():
        #     joins += r[1]
        #     leaves += r[2]
        # self.render(
        #     "index.html",
        #     group_num=len(util.get_group_names()),
        #     group_mbr_num=len(util.get_group_mbrs()),
        #     unique_group_mbr_num=len(util.get_unique_group_mbrs()),
        #     joins=joins,
        #     leaves=leaves,
        # )
        pass


class GroupHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class PersonHandler(tornado.web.RequestHandler):
    """
    个人基本信息
    昵称，备注，头像，性别，位置
    加入了的群，每个群一共发了多少消息，今天发了多少消息

    """

    def get(self):
        print("\n\n\n")
        nickname = self.get_argument("nickname", None)
        if not nickname:
            iql = 'select count(content) from message group by "nickname"'
            mbrs = influx_client.query(iql)
            nums = list(mbrs.get_points())
            names = mbrs.keys()
            mbrs = []
            for idx in range(len(names)):

                iql = "select first(nickname_m) from message where nickname='{}'".format(names[idx][1]["nickname"])
                print(iql)
                earliest = list(influx_client.query(iql).get_points())[0]["time"].replace("T", " ").split(".")[0]
                print(earliest)

                iql = "select last(nickname_m) from message where nickname='{}'".format(names[idx][1]["nickname"])
                print(iql)
                latest = list(influx_client.query(iql).get_points())[0]["time"].replace("T", " ").split(".")[0]
                print(latest)

                mbrs.append([names[idx][1]["nickname"], earliest, latest, nums[idx]["count"]])
            print(mbrs)
            self.render("person_list.html", mbrs=mbrs)
        print(nickname)

        iql = "select * from message where nickname='{}';".format(nickname)
        print(iql)
        msgs = influx_client.query(iql)
        msgs = list(msgs.get_points())
        msgs = [[m["time"].split(".")[0].replace("T", " "), m["group"], m["content"]] for m in msgs]
        print(msgs)

        iql = "select count(group_m) from message where nickname='{}' group by \"group\";".format(nickname)
        print(iql)
        msg_count = influx_client.query(iql)
        keys = msg_count.keys()
        points = list(msg_count.get_points())
        groups = []
        for idx in range(len(keys)):
            # print(keys[idx][1]["group"])
            # print(points[idx]["count"])
            groups.append([keys[idx][1]["group"], points[idx]["count"]])
        print(groups)

        iql = "select count(group_m) from message where nickname='{}' group by time(1d)".format(nickname)
        print(iql)
        msg_agg = influx_client.query(iql)
        msg_agg = list(msg_agg.get_points())
        msg_agg = [[d["time"].split("T")[0], d["count"]] for d in msg_agg]
        print(msg_agg)

        iql = "select distinct(groupnick) from nick where nickname='{}'".format(nickname)
        print(iql)
        nicks = list(influx_client.query(iql).get_points())
        nicks = [n["distinct"] for n in nicks]
        print(nicks)

        self.render("person.html", msgs=msgs, groups=groups, nickname=nickname, msg_agg=msg_agg, nicks=nicks)


class AllMessages(tornado.web.RequestHandler):
    """测试用，显示所有消息"""

    def get(self):
        res = influx_client.query("select * from message;")
        self.write(res[0])


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/group", GroupHandler),
            (r"/person", PersonHandler),
            (r"/msg", AllMessages),
        ]
        tornado.web.Application.__init__(
            self,
            handlers,
            template_path=os.path.join(
                os.path.dirname(__file__),
                "template",
            ),
            static_path=os.path.join(os.path.dirname(__file__), "upload"),
        )


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
