# 针对拉勾的爬虫

## 要求

1. 本地安装 Chrome 浏览器
2. 清楚 Chrome 的版本
3. 下载对应的 [ChromeDriver](https://chromedriver.chromium.org/downloads)
4. 在命令行中执行命令

## 步骤

1. 运行 Chrome，监听在 9222 端口（爬虫中使用）

Mac 上如下运行：

```shell
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

Windows 上如下运行：

```shell
start chrome --remote-debugging-port=9222
```

![LhNqFe](https://oss.images.shujudaka.com/uPic/LhNqFe.png)

2. 在启动的浏览器中(注意，不是系统默认的)，打开 lagou.com 登录用户(要不然也会让你登录的)

![nZ0Egv](https://oss.images.shujudaka.com/uPic/nZ0Egv.png)

3. 启动 main.py

4. 输入要查询的职位

5. 输入要搜索的地区