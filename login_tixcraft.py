from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import secret

email = secret.email
passwd = secret.passwd
driver = webdriver.Chrome()


def login_google():
    driver.get("https://accounts.google.com/signin")
    driver.implicitly_wait(3)

    driver.find_element_by_id("identifierId").send_keys(email)
    driver.find_element_by_id("identifierNext").click()

    driver.implicitly_wait(8)
    
    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@type="password"]'))
    )

    password.send_keys(passwd)

    element = driver.find_element_by_id("passwordNext")
    driver.execute_script("arguments[0].click();", element)


def login_tixcraft():
    sleep(3)
    driver.get("https://tixcraft.com/login/google")
    # sleep(3)
    # driver.get("https://tixcraft.com/user/changeLanguage/lang/zh_tw")
    cookies = driver.get_cookies()
    save_cookie(cookies)


def save_cookie(cookies):
    with open("session.json", "w") as f:
        json.dump(cookies, f)


def main():
    if email == "your_email" or passwd == "your_passwd":
        print("請先在secret.py中，修改為自己的帳號與密碼")
        return

    login_google()
    login_tixcraft()
    driver.close()


if __name__ == "__main__":
    main()
