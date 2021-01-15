from hoshino.service import Service
from hoshino import *
import json

json_path="C:/tmp/zfjdhj.github.io/zfjbot-helpWebsite/data.json"

sv = Service('zfjbot-helpSearch')

# 读取json文件内容,返回字典格式
with open(json_path,'r',encoding='utf8')as fp:
    json_data = json.load(fp)
    # print('这是文件中的json数据：',json_data)
    # print('这是读取到文件数据的数据类型：', type(json_data))

@sv.on_rex(r'^(help|帮助) (.*)$')
async def search(bot,ev):
    reply=''
    res=[]
    if ev['match'].group(2).strip():
        keyword=ev['match'].group(2).strip()
        logger.info(f'help search {keyword}')
        # await bot.send(ev,keyword)
        # return
        if keyword and type(json_data) == list :
            for plugin_type in json_data:
                for plugin in plugin_type['plugins_list']:
                    # print(plugin['plugin_name'])
                    for commands in plugin['plugin_commands']:
                        # print(commands['command'])
                        if commands['command'].find(keyword) != -1:
                            res.append({'plugin_name':plugin['plugin_name'],'command':commands['command'],'description':commands['description']})
                            continue
                        # print(commands['description'])
                        if commands['description'].find(keyword) != -1:
                            res.append({'plugin_name':plugin['plugin_name'],'command':commands['command'],'description':commands['description']})
                            continue
        logger.info(f'res in search: {len(res)}')
        if len(res) >0:
            for item in res:
                reply += f"{item['command']}: {item['description']}\n"
            reply +=f'============\n猫猫共查询到结果{len(res)}条'
            await bot.send(ev,reply)
        else:
            await bot.send(ev,'猫猫没有找到呢~喵~')
