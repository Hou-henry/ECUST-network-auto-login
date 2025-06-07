# ECUST Network Auto Login

这是一个基于 Selenium 的自动登录华东理工大学校园网的 Python 脚本，支持定时检测网络状态并在掉线后自动重新登录。

## 🚀 功能特点

- 基于 Selenium 自动化模拟登录校园网
- 每 60 秒自动检测网络是否掉线
- 检测到掉线后自动执行登录流程
- 支持 Headless（无头）模式，适用于服务器或后台运行

## 📦 环境依赖

- Python 3.8+
- [ChromeDriver](https://sites.google.com/chromium.org/driver/)（需与本地 Chrome 浏览器版本匹配）
- Python 库：selenium

安装依赖：

```bash
pip install selenium python-dotenv
```

## 🧠 使用说明

1. 项目中已经有137版本的，如果需要其他版本，请下载并解压 ChromeDriver，将其放置在项目根目录下（或修改脚本路径）

2. 运行脚本（首次运行会提示输入账号密码）：

```bash
python main.py
```

```bash
# 在服务器机房中的网络
python main_server.py
```

> 💡 第一次运行程序时，如果 `.env` 文件中没有配置账号和密码，程序会提示你输入，并自动将其保存到 `.env` 文件中。后续运行将直接读取该文件内容。

3. 脚本将持续在后台运行，并每 60 秒（默认值，可通过参数调整）检测一次网络连接状态。

## 📁 项目结构

```
.
├── main.py         # 自动登录主程序
├── main.py         # 自动登录主程序（服务器机房环境）
├── chromedriver    # Chrome 浏览器驱动
├── README.md       # 使用说明文件
```

## ⚠️ 安全提示

- **不要将含有账号密码的代码上传到 GitHub**
- 推荐将账号密码提取到 `.env` 文件，并使用 `python-dotenv` 加载

## 📄 License

MIT License