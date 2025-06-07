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

def login(username, password):
    """
    执行自动登录操作（适配新版 Srunsoft 页面）
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 第一步：访问外网地址，触发校园网网关重定向
        driver.get("http://www.baidu.com")
        time.sleep(2)

        # 第二步：记录重定向后的登录页面地址
        real_login_url = driver.current_url
        print("跳转后的URL：", real_login_url)

        # 第三步：重新访问认证页面，确保页面完整加载
        driver.get(real_login_url)
        time.sleep(2)

        wait = WebDriverWait(driver, 10)

        # 填写用户名
        username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input.clear()
        username_input.send_keys(username)

        # 填写密码
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)

        # 设置上网类型（@free or 空）
        driver.execute_script("""
            var domain = document.querySelector("input[name='net-type']:checked").value;
            document.getElementById("domain").value = domain;
        """)

        # 点击登录按钮
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login")))
        login_button.click()

        time.sleep(3)
        print("登录操作完成")

    except Exception as e:
        print("登录异常:", e)
        print(driver.page_source)  # 打印当前页面源码帮助调试
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
    while True:
        if not is_logged_in():
            print("未登录，开始自动登录...")
            login(username,password)
        else:
            print("网络已登录，无需操作")
        time.sleep(60)  # 每60秒检测一次