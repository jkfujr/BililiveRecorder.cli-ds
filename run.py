# ssl相关
import ssl
from ssl import SSLContext
from typing import Dict, List

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 引用api文件
from config.api import BililiveRec_API_LIST

app = FastAPI()

# 静态文件
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
# html文件
webui = Jinja2Templates(directory="webui")


# 访问地址/(根路径)返回HTML页面
@app.get("/")
async def root(request: Request):
    # 获取已排序数据
    sorted_data = get_data()
    # 渲染到网页
    return webui.TemplateResponse("index.html", {"request": request, "data": sorted_data})


@app.get("/bililiveRec/api")
async def get_bililiveRec_room_all():
    # 获取已排序数据
    sorted_data = get_data()
    # 返回数据
    return {"data": sorted_data}


@app.get("/bililiveRec/api/{object_id}")
async def get_bililiveRec_room(object_id: str):
    all_data = get_all_data()
    # 筛选需要的数据
    data = next(filter(lambda x: x.get("objectId") ==
                object_id, all_data), None)
    # 判断直播间存不存在，不存在返回404
    if data is not None:
        formatted_data = format_data_single(data)
        return formatted_data
    else:
        raise HTTPException(status_code=404, detail="直播间不存在")


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


def format_data_single(d: Dict) -> Dict:

    formatted_data = {  # 存储格式化后的单个数据字典
        "录播姬ID": d.get("objectId"),
        "直播间ID": d.get("roomId"),
        "用户名": d.get("name"),
        "直播间标题": d.get("title"),
        "直播状态": d.get("streaming"),
        "录制状态": d.get("recording")
    }
    return formatted_data


def sort_data(data: List[Dict]) -> List[Dict]:
    return sorted(data, key=lambda x: x["用户名"])


if __name__ == "__main__":

    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=9101,
        # ssl相关，不需要就注释掉
        ssl_keyfile="./ssl/wll.114514.plus.key",
        ssl_certfile="./ssl/wll.114514.plus.crt",
        log_level="info",
        reload=True
    )
