import requests
import pymysql
import time

# 引用api文件
from config.api import BililiveRec_API_LIST

# 连接MySQL数据库
conn = pymysql.connect(host='10.0.0.111',
                       port=3306,
                       user='test_bilirec',
                       passwd='QRS@ExpXo$fzn7L!',
                       db='test_bilirec',
                       charset='utf8mb4',
                       connect_timeout=600)
# 创建游标
cur = conn.cursor()


# 循环读取API地址
for api_url in BililiveRec_API_LIST:
    try:
        resp = requests.get(api_url, timeout=10)
        # 请求成功
        if resp.status_code == requests.codes.ok:
            # 把数据转为JSON格式
            data_json = resp.json()
            # 创建一个列表，用于存储从 API 获取到的解析后的数据
            all_data = []
            # 循环遍历解析后的数据，存储到 all_data 中
            for data in data_json:
                fields = {
                    '直播间ID': data['roomId'],
                    '用户名': data['name'],
                    '直播间标题': data['title'],
                    '直播间短ID': data['shortId'],
                    '一级直播分区': data['areaNameParent'],
                    '二级直播分区': data['areaNameChild'],
                    '是否启用自动录制': int(data['autoRecord']),
                    '是否在录制': int(data['recording']),
                    '是否在直播': int(data['streaming']),
                    '会话时长': data['recordingStats']['sessionDuration'],
                    '总接受字节数': data['recordingStats']['totalInputBytes'],
                    '总写入字节数': data['recordingStats']['totalOutputBytes'],
                    '当前文件的大小': data['recordingStats']['currentFileSize'],
                    '总时长': data['recordingStats']['sessionMaxTimestamp'],
                    '直播服务器域名': data['ioStats']['streamHost'],
                    '创建时间': int(time.time() * 1000),
                    '更新时间': int(time.time() * 1000)
                }
                all_data.append(fields)
        else:
            print('请求成功，状态码为：', resp.status_code)
    except requests.exceptions.Timeout:
        print('请求超时，检查API')
    # 定义函数，将获取到的数据插入数据库
    for data in all_data:
        # 根据"直播间ID"字段与最新的自增id查询所有直播间最新的数据
        cur.execute(
            "SELECT * FROM user_data WHERE roomId=%s AND id=(SELECT MAX(id) FROM user_data WHERE roomId=%s)",
            (data['直播间ID'], data['直播间ID']))
        db_data = cur.fetchone()
        # print(db_data)

        if db_data:
            # 如果 API数据 中对应直播间 未开播，
            if data['是否在直播'] == 0:
                # 数据库 中对应直播间数据 未开播，则跳过对应直播间该行的数据，不更新不创建；
                if db_data[9] == 0:
                    continue
                # 数据库 中对应直播间 开播，则使用 API数据 的数据更新数据库里对应直播间行的数据。
                else:
                    cur.execute("""UPDATE user_data SET title=%s, areaNameParent=%s, areaNameChild=%s, streaming=%s, recording=%s, utime=%s WHERE roomId=%s AND id=(SELECT MAX(id) FROM user_data WHERE roomId=%s)""",
                    (data['直播间标题'], data['一级直播分区'], data['二级直播分区'], data['是否在直播'], data['是否在录制'], data['更新时间'], data['直播间ID'], data['直播间ID']))
                    conn.commit()
            # 如果 API数据 中对应直播间数据 直播中，
            else:
                # 数据库 中对应直播间数据 未开播，使用 API数据，新创建一行数据
                if db_data[9] == 0:
                    cur.execute("INSERT INTO user_data (roomId, name, title, shortId, areaNameParent, areaNameChild, autoRecord, recording, streaming, sessionDuration, totalInputBytes, totalOutputBytes, currentFileSize, sessionMaxTimestamp, streamHost, ctime, utime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (data['直播间ID'], data['用户名'], data['直播间标题'], data['直播间短ID'], data['一级直播分区'], data['二级直播分区'], data['是否启用自动录制'], data['是否在录制'], data['是否在直播'], data['会话时长'], data['总接受字节数'], data['总写入字节数'], data['当前文件的大小'], data['总时长'], data['直播服务器域名'], data['创建时间'], data['更新时间']))
                    conn.commit()
                # 数据库 中对应直播间数据 直播中
                else:
                    # 如果 API数据 中对应直播间的 "会话时长" 大于 数据库 中对应直播间的 "sessionDuration(会话时长)" 字段，
                    # 则使用 API数据 中对应直播间的数据更新 数据库 里对应直播间行数据中的 "sessionDuration"、"totalInputBytes"、"totalOutputBytes"、"currentFileSize"、"sessionMaxTimestamp"、"streamHost" 这几个字段。
                    if db_data[10] < data['会话时长']:
                        cur.execute("""UPDATE user_data SET sessionDuration=%s, totalInputBytes=%s, totalOutputBytes=%s, currentFileSize=%s, sessionMaxTimestamp=%s, streamHost=%s, utime=%s WHERE roomId=%s AND id=(SELECT MAX(id) FROM user_data WHERE roomId=%s)""",
                                    (data['会话时长'], data['总接受字节数'], data['总写入字节数'], data['当前文件的大小'], data['总时长'], data['直播服务器域名'], data['更新时间'], data['直播间ID'], data['直播间ID']))
                        conn.commit()
                    else:
                        # 如果 API数据 中对应直播间的 "会话时长" 小于 数据库 中对应直播间的 "sessionDuration(会话时长)" 字段，
                        # 则使用"all_data"中对应直播间的数据更新数据库里对应直播间行数据中的 "streaming"、"recording"、"utime" 这三个字段，并使用"all_data"中对应直播间的数据，创建新一行数据。
                        cur.execute("""UPDATE user_data SET streaming=%s, recording=%s, utime=%s WHERE roomId=%s AND id=(SELECT MAX(id) FROM user_data WHERE roomId=%s)""",
                            (data['是否在直播'], data['是否在录制'], data['更新时间'], data['直播间ID'], data['直播间ID']))
                        conn.commit()
                        # 创建新一行数据。
                        cur.execute("INSERT INTO user_data (roomId, name, title, shortId, areaNameParent, areaNameChild, autoRecord, recording, streaming, sessionDuration, totalInputBytes, totalOutputBytes, currentFileSize, sessionMaxTimestamp, streamHost, ctime, utime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (data['直播间ID'], data['用户名'], data['直播间标题'], data['直播间短ID'], data['一级直播分区'], data['二级直播分区'], data['是否启用自动录制'], data['是否在录制'], data['是否在直播'], data['会话时长'], data['总接受字节数'], data['总写入字节数'], data['当前文件的大小'], data['总时长'], data['直播服务器域名'], data['创建时间'], data['更新时间']))
                        conn.commit()
        else:
            # 如果数据库对应直播间"roomId"字段中没有"all_data"中"直播间ID"字段对应的数据，则插入对应新一行数据
            cur.execute("INSERT INTO user_data (roomId, name, title, shortId, areaNameParent, areaNameChild, autoRecord, recording, streaming, sessionDuration, totalInputBytes, totalOutputBytes, currentFileSize, sessionMaxTimestamp, streamHost, ctime, utime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (data['直播间ID'], data['用户名'], data['直播间标题'], data['直播间短ID'], data['一级直播分区'], data['二级直播分区'], data['是否启用自动录制'], data['是否在录制'], data['是否在直播'], data['会话时长'], data['总接受字节数'], data['总写入字节数'], data['当前文件的大小'], data['总时长'], data['直播服务器域名'], data['创建时间'], data['更新时间']))
            conn.commit()


# 关闭 cursor 和连接
cur.close()
conn.close()
