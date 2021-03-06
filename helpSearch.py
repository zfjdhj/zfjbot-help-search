"""
Author: zfj
Date: 2021-03-06 16:17:46
LastEditTime: 2021-03-06 16:17:46
LastEditors: zfj
Description: None
GitHub: https://github.com/zfjdhj
"""
from hoshino.service import Service
from hoshino import *
import json

json_path = "C:/tmp/zfjdhj.github.io/zfjbot-helpWebsite/data.json"

sv = Service("zfjbot-helpSearch")

# 读取json文件内容,返回字典格式
with open(json_path, "r", encoding="utf8") as fp:
    json_data = json.load(fp)


@sv.on_rex(r"^(help|帮助) (.*)$")
async def search(bot, ev):
    global json_data
    reply = ""
    res = []
    if ev["match"].group(2).strip():
        keyword = ev["match"].group(2).strip()
        logger.info(f"help search {keyword}")
        # await bot.send(ev,keyword)
        # return
        if keyword and type(json_data) == list:
            for plugin_type in json_data:
                for plugin in plugin_type["plugins_list"]:
                    if plugin["plugin_state"] == "禁用":
                        continue
                    elif plugin["plugin_name"].find(keyword) != -1:
                        for commands in plugin["plugin_commands"]:
                            res.append(
                                {
                                    "plugin_name": plugin["plugin_name"],
                                    "command": commands["command"],
                                    "description": commands["description"],
                                }
                            )
                        continue
                    else:
                        # print(plugin['plugin_name'])
                        for commands in plugin["plugin_commands"]:
                            # print(commands['command'])
                            if commands["command"].find(keyword) != -1:
                                res.append(
                                    {
                                        "plugin_name": plugin["plugin_name"],
                                        "command": commands["command"],
                                        "description": commands["description"],
                                    }
                                )
                                continue
                            # print(commands['description'])
                            if commands["description"].find(keyword) != -1:
                                res.append(
                                    {
                                        "plugin_name": plugin["plugin_name"],
                                        "command": commands["command"],
                                        "description": commands["description"],
                                    }
                                )
                                continue
        logger.info(f"res in search: {len(res)}")
        # if len(res) > 0:
        #     for index, item in enumerate(res):
        #         reply += f"{index+1}. {item['command']}: {item['description']}\n"
        #     reply += f"============\n猫猫共查询到结果{len(res)}条"
        #     await bot.send(ev, reply)

        if 0 < len(res) <= 20:
            for index, item in enumerate(res):
                reply += f"{index+1}. {item['command']}: {item['description']}\n"
            reply += f"============\n猫猫共查询到结果{len(res)}条"
            await bot.send(ev, reply)
        elif 20 < len(res) <= 60:
            li = []
            for index, item in enumerate(res):
                reply += f"{index+1}. {item['command']}: {item['description']}\n"
                if (index + 1) % 20 == 0:
                    data = {"type": "node", "data": {"name": "猫猫", "uin": "1475166415", "content": reply}}
                    li.append(data)
                    reply = ""
            reply += f"============\n猫猫共查询到结果{len(res)}条"
            data = {"type": "node", "data": {"name": "猫猫", "uin": "1475166415", "content": reply}}
            li.append(data)
            gid = ev.group_id
            await bot.send_group_forward_msg(group_id=gid, messages=li)
        elif 60 < len(res):
            li = []
            for index, item in enumerate(res):
                reply += f"{index+1}. {item['command']}: {item['description']}\n"
                if (index + 1) % 5 == 0:
                    data = {"type": "node", "data": {"name": "猫猫", "uin": "1475166415", "content": reply}}
                    li.append(data)
                    reply = ""
            reply += f"============\n猫猫共查询到结果{len(res)}条"
            data = {"type": "node", "data": {"name": "猫猫", "uin": "1475166415", "content": reply}}
            li.append(data)
            gid = ev.group_id
            await bot.send_group_forward_msg(group_id=gid, messages=li)
        else:
            with open(json_path, "r", encoding="utf8") as fp:
                json_data = json.load(fp)
            await bot.send(ev, "猫猫没有找到呢~喵~\n请再次尝试或者联系管理员")
