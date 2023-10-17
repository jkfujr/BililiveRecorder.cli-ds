# 简介

![截图_2023-04-20_04-01-56](https://user-images.githubusercontent.com/39889850/233187311-206378ae-4770-404d-bbf2-45a6cf0ec491.png)


一个用 python 实现的"多"录播姬命令行简单的信息展示

演示 [https://wll.114514.plus:11111/](https://wll.114514.plus:11111/)

    演示后端数据使用数据库存储(测试)，打不开的话可能是我在写啥东西 (比github上的新

## 使用说明

1. 需要Python 3.10及以上版本

2. 安装依赖

```
pip install -r requirements.txt

# 支持SSL (可选)
pip install SSLContext
```

3. 添加 API

```
# 编辑 `./config/rec_api.py` 文件

# 录播姬的api
BililiveRec_API_LIST = [
    "http://录播姬A的IP:端口/api/room",
    "http://录播姬B的IP:端口/api/room"
]
```

4. 运行

```
# Windows
双击 run.bat

# Linux
$ python main.py
```

5. 访问 [http://127.0.0.1:9101](http://127.0.0.1:9101) (默认)



## 更新计划(饼)

- 数据库 (测试中)
- 日志
- 缓存机制
- 录播姬管理

## 联系方式

Rec-NIC 今天也是咕咕咕的一天 [722935608](https://jq.qq.com/?_wv=1027&k=KI1Ly3kG)

    (录播姬非官方闲聊群但是官方)

## 相关项目

> BililiveRecorder https://github.com/Bililive/BililiveRecorder
> 
> BililiveRecorder-WebUI https://github.com/BililiveRecorder/BililiveRecorder-WebUI
