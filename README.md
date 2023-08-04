# 简介

![截图_2023-04-20_04-01-56](https://user-images.githubusercontent.com/39889850/233187311-206378ae-4770-404d-bbf2-45a6cf0ec491.png)


一个用 python 实现的"多"录播姬命令行简单的信息展示

演示 [https://wll.114514.plus:11111/](https://wll.114514.plus:11111/)

    演示后端数据使用数据库存储(测试)，打不开的话可能是我在写啥东西 (比github上的新

## 一、要求

- Python 3.10

```
# 需要以下模块
fastapi、uvicorn、Jinja2、
SSLContext(支持SSL，可选)
```

## 二、使用

### 1. 下载

### 2. 添加 API

```
# 编辑 `./config/api.py` 文件

# 录播姬的api
BililiveRec_API_LIST = [
    "http://录播姬A的IP:端口/api/room",
    "http://录播姬B的IP:端口/api/room"
]
```

### 3. 运行

#### Windows

```
双击 run.bat
```

#### Linux

```
$ python main.py
```

### 4. 访问 [http://127.0.0.1:9101](http://127.0.0.1:9101)

(默认的情况下)

## 三、更新计划(饼)

```
- 数据库 (测试中)
- 日志
- 缓存机制
```

## 四、联系

Rec-NIC 今天也是咕咕咕的一天 [722935608](https://jq.qq.com/?_wv=1027&k=KI1Ly3kG)

    (录播姬非官方闲聊群但是官方)

## 五、相关

> BililiveRecorder https://github.com/Bililive/BililiveRecorder
> 
> BililiveRecorder-WebUI https://github.com/BililiveRecorder/BililiveRecorder-WebUI
