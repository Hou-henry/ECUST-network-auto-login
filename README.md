

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
pip install selenium
```

## 🧠 使用说明

1. 下载并解压 ChromeDriver，将其放置在项目根目录下（或修改脚本路径）

2. 修改 `main.py`，将账号密码填入对应位置：

```python
username_input.send_keys("你的校园网账号")
password_input.send_keys("你的密码")
```

⚠️ **建议使用 `.env` 文件或配置文件方式存储账号密码，避免泄露！**

3. 运行脚本：

```bash
python main.py
```

脚本将持续在后台运行，并每 60 秒检测一次网络连接状态。

## 📁 项目结构

```
.
├── main.py         # 自动登录主程序
├── chromedriver    # Chrome 浏览器驱动（需手动下载）
├── README.md       # 使用说明文件
```

## ⚠️ 安全提示

- **不要将含有账号密码的代码上传到 GitHub**
- 推荐将账号密码提取到 `.env` 文件，并使用 `python-dotenv` 加载

## 📌 未来改进计划（TODO）

- [ ] 环境变量或配置文件管理账号密码
- [ ] 登录状态日志记录
- [ ] 命令行参数设置检测间隔与登录地址
- [ ] GUI 配置界面

## 📄 License

MIT License