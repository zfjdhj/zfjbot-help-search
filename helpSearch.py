import json



json_path="./data.json"






s='查'
res=[]


# 读取json文件内容,返回字典格式
with open(json_path,'r',encoding='utf8')as fp:
    json_data = json.load(fp)
    # print('这是文件中的json数据：',json_data)
    # print('这是读取到文件数据的数据类型：', type(json_data))

if type(json_data) == list:
    for plugin_type in json_data:
        for plugin in plugin_type['plugins_list']:
            # print(plugin['plugin_name'])
            for commands in plugin['plugin_commands']:
                # print(commands['command'])
                if commands['command'].find(s) != -1:
                    res.append({'plugin_name':plugin['plugin_name'],'command':commands['command'],'description':commands['description']})
                    break
                # print(commands['description'])
                if commands['description'].find(s) != -1:
                    res.append({'plugin_name':plugin['plugin_name'],'command':commands['command'],'description':commands['description']})
                    break
print(len(res))
for item in res:
    print(item)