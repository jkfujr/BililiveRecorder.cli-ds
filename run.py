
import ssl
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from ssl import SSLContext
from config.api import BililiveRec_API_LIST
from typing import Dict, List


import requests
import uvicorn

app = FastAPI()

# 静态文件
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
# html文件
webui = Jinja2Templates(directory="webui")


# 访问地址/(根路径)返回HTML页面
@app.get("/")
async def root(request: Request):
    # 存储解析后的所有数据
    all_data = []

    # 请求所有API，并将数据整合到 all_data 变量中
    for api in BililiveRec_API_LIST:
        response = requests.get(api)

        if response.status_code == 200:
            all_data.extend(response.json())

    # 格式化和排序数据
    formatted_data = format_data(all_data)
    sorted_data = sort_data(formatted_data)

    return webui.TemplateResponse("index.html", {"request": request, "data": sorted_data})


# 返回所有直播间的数据
@app.get("/bililiveRec/api")
async def get_bililiveRec_room_all():
    # 存储解析后的所有数据
    all_data = []

    # 请求所有API，并将数据整合到 all_data 变量中
    for api in BililiveRec_API_LIST:
        response = requests.get(api)

        if response.status_code == 200:
            all_data.extend(response.json())

    # 格式化和排序数据
    formatted_data = format_data(all_data)
    sorted_data = sort_data(formatted_data)

    return {"data": sorted_data}


# 返回指定直播间的数据
@app.get("/bililiveRec/api/{object_id}")
async def get_bililiveRec_room(object_id: str):

    # 存储解析后的所有数据
    all_data = []

    # 请求所有API，并将数据整合到 all_data 变量中
    for api in BililiveRec_API_LIST:
        response = requests.get(api)

        if response.status_code == 200:
            all_data.extend(response.json())

    # 从 all_data 变量中查询指定直播间
    data = next(filter(lambda x: x.get("objectId")
                == object_id, all_data), None)

    if data is not None:
        # 将数据重新格式化为所需的格式
        formatted_data = {
            "录播姬ID": data.get("objectId"),
            "直播间ID": data.get("roomId"),
            "用户名": data.get("name"),
            "直播间标题": data.get("title"),
            "直播状态": data.get("streaming"),
            "录制状态": data.get("recording")
        }
        return formatted_data
    else:
        # 如果直播间不存在，返回404错误
        raise HTTPException(status_code=404, detail="直播间不存在")


def format_data(data: List[Dict]) -> List[Dict]:
    # 将API返回的数据重新格式化为所需的格式
    formatted_data = []

    for d in data:
        formatted_data.append({
            "录播姬ID": d.get("objectId"),
            "直播间ID": d.get("roomId"),
            "用户名": d.get("name"),
            "直播间标题": d.get("title"),
            "直播状态": d.get("streaming"),
            "录制状态": d.get("recording")
        })

    return formatted_data


# 对数据按照用户名升序进行排序
def sort_data(data: List[Dict]) -> List[Dict]:

    return sorted(data, key=lambda x: x["用户名"])



if __name__ == "__main__":
    
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=9101,
        # 不需要SSL就注释掉
        ssl_keyfile="./ssl/wll.114514.plus.key",
        ssl_certfile="./ssl/wll.114514.plus.crt",
        log_level="info",
        reload=True
    )
