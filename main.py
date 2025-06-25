from datetime import datetime

import json
import os
import platform
from dotenv import load_dotenv
from pathlib import Path
from dotenv import set_key
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

env_path = Path(".env")
if not env_path.exists():
    env_path.touch()

load_dotenv()

system_name = platform.system()
if system_name == "Windows":
    chrome_driver_path = "./chromedriver_win.exe"
elif system_name == "Darwin":  # macOS
    chrome_driver_path = "./chromedriver_mac"
else:  # Assume Linux
    chrome_driver_path = "./chromedriver_linux"

def is_logged_in():
    """
    简单检测网络是否已经登录校园网。
    这里用访问百度，判断是否被重定向到登录页，或者页面标题包含校园网提示。
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get("http://www.baidu.com")
        time.sleep(2)
        current_url = driver.current_url
        print("检测网络，当前URL:", current_url)
        # 根据实际判断逻辑调整
        if "srun_portal" in current_url or "login" in current_url:
            return False  # 说明未登录，跳转到了认证页面
        else:
            return True
    except Exception as e:
        print("检测网络异常:", e)
        return False
    finally:
        driver.quit()

def login(username,password):
    """
    执行自动登录操作
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        # 访问外网触发重定向
        driver.get("http://www.baidu.com")
        time.sleep(2)

        current_url = driver.current_url
        print("登录流程，当前URL:", current_url)

        if "baidu" in current_url:
            driver.get("http://172.20.3.90:804/srun_portal_pc.php")
            time.sleep(2)

        wait = WebDriverWait(driver, 10)
        username_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username_input.clear()
        username_input.send_keys(username)

        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)

        login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()

        time.sleep(3)
        print("登录操作完成")
    except Exception as e:
        print("登录异常:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    # 命令行参数解析后检查用户名和密码
    username = os.getenv("CAMPUS_USERNAME")
    password = os.getenv("CAMPUS_PASSWORD")
    if not username:
        username = input("请输入校园网账号：")
        set_key(".env", "CAMPUS_USERNAME", username)
    if not password:
        password = input("请输入校园网密码：")
        set_key(".env", "CAMPUS_PASSWORD", password)
last_login_time = None  # 初始化上次登录时间

while True:
    if not is_logged_in():
        now = datetime.now()
        print("未登录，开始自动登录...")

        # 计算上次登录间隔
        if last_login_time is not None:
            elapsed = (now - last_login_time).total_seconds()
        else:
            elapsed = None

        # 执行登录操作
        login(username, password)

        # 记录当前时间为上次登录时间
        previous_login_str = last_login_time.strftime("%Y-%m-%d %H:%M:%S") if last_login_time else None
        last_login_time = now

        # 构造日志数据
        log_data = {
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": previous_login_str,
            "elapsed_min": int(elapsed)/60 if elapsed is not None else None
        }

        # 控制台输出 JSON 日志
        print(json.dumps(log_data, ensure_ascii=False, indent=2))

        # 写入文件
        with open("login_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + "\n")

    else:
        print("网络已登录，无需操作")

    time.sleep(60)
