import datetime
import requests
from typing import Dict, List
# 引用api文件
# from api import BililiveRec_API_LIST
from config.api import BililiveRec_API_LIST


def get_data() -> List[Dict]:
    # 存储解析后的所有数据
    all_data = []
    # 请求所有API，并将数据整合到all_data变量中
    for api in BililiveRec_API_LIST:
        response = requests.get(api)
        # 如果请求成功，将请求获取到的数据拼接到all_data中
        if response.status_code == 200:
            all_data.extend(response.json())
    # 格式化和排序数据
    formatted_data = format_data(all_data)
    sorted_data = sort_data(formatted_data)
    return sorted_data


def get_all_data() -> List[Dict]:
    # 存储解析后的所有数据
    all_data = []
    # 请求所有API，并将数据整合到all_data变量中
    for api in BililiveRec_API_LIST:
        response = requests.get(api)
        # 如果请求成功，将请求获取到的数据拼接到all_data中
        if response.status_code == 200:
            all_data.extend(response.json())
    return all_data


def format_data(data: List[Dict]) -> List[Dict]:
    # 存储格式化后的数据
    formatted_data = []
    for d in data:
        # 调用format_data_single函数，格式化单个录播姬数据并添加到列表
        formatted_data.append(format_data_single(d))
    return formatted_data





def format_data_single(data: Dict) -> Dict:

    # 时间格式化
    sessionDuration_duration_ms = round(float(data.get("recordingStats")["sessionDuration"]))
    sessionMaxTimestamp_duration_ms = round(float(data.get("recordingStats")["sessionMaxTimestamp"]))
    

    sessionDuration = datetime.timedelta(milliseconds=sessionDuration_duration_ms)
    sessionMaxTimestamp = datetime.timedelta(milliseconds=sessionMaxTimestamp_duration_ms)

    formatted_data = {
        "录播姬ID": data.get("objectId"),
        "直播间ID": data.get("roomId"),
        "一级直播分区": data.get("areaNameParent"),
        "二级直播分区": data.get("areaNameChild"),
        # 是否开启自动录制
        "自动录制": data.get("autoRecord"),
        "用户名": data.get("name"),
        "直播间标题": data.get("title"),
        "直播状态": data.get("streaming"),
        "录制状态": data.get("recording"),
        "会话时长": str(sessionDuration).split(".")[0],
        "总接受字节数": data.get("recordingStats")["totalInputBytes"],
        "总写入字节数": data.get("recordingStats")["totalOutputBytes"],
        "当前文件的大小": data.get("recordingStats")["currentFileSize"],
        "总时长": str(sessionMaxTimestamp).split(".")[0],
        "直播服务器域名": data.get("ioStats")["streamHost"],
        }
    return formatted_data


def sort_data(data: List[Dict]) -> List[Dict]:
    return sorted(data, key=lambda x: x["用户名"])


