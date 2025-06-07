from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_driver_path = "./chromedriver"  # 替换为你的实际 chromedriver 路径

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

def login():
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
        username_input.send_keys("Y80230044")

        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys("09190015Ecust#")

        login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()

        time.sleep(3)
        print("登录操作完成")
    except Exception as e:
        print("登录异常:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        if not is_logged_in():
            print("未登录，开始自动登录...")
            login()
        else:
            print("网络已登录，无需操作")
        time.sleep(60)  # 每60秒检测一次