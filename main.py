# ssl相关
import ssl
from ssl import SSLContext
from typing import Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 引用整理好的数据
from config.data import get_data
from config.data import get_all_data
from config.data import format_data_single

app = FastAPI(
    docs_url=None,
    redoc_favicon_url="/webui/assets/logo.ico",
)


# 静态文件
app.mount("/assets", StaticFiles(directory="./webui/assets"), name="assets")
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


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9101,
        # ssl相关，不需要就注释掉
        ssl_keyfile="./ssl/wll.114514.plus.key",
        ssl_certfile="./ssl/wll.114514.plus.crt",
        log_level="info",
        reload=True
    )
