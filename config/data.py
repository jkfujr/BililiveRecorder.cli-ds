import requests
from typing import Dict, List
# 引用api文件
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

    formatted_data = {  # 存储格式化后的单个数据字典
        "录播姬ID": data.get("objectId"),
        "直播间ID": data.get("roomId"),
        "用户名": data.get("name"),
        "直播间标题": data.get("title"),
        "直播状态": data.get("streaming"),
        "录制状态": data.get("recording")
    }
    return formatted_data


def sort_data(data: List[Dict]) -> List[Dict]:
    return sorted(data, key=lambda x: x["用户名"])
