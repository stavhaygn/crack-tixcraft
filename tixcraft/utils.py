from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests


def login():
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)
    driver.get("https://tixcraft.com/login")
    WebDriverWait(driver, 600).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@class='user-name']"))
    )
    cookies = driver.get_cookies()
    driver.quit()
    return cookies


def user_verify(driver, url):
    driver.get(url)
    url = driver.current_url
    while "ticket/verify" in url:
        try:
            url = driver.current_url
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to_alert()
            alert.accept()
        except:
            pass
    return url


def session_to_driver(session):
    cookies = session.cookies.get_dict()
    driver = webdriver.Chrome()
    driver.get("https://tixcraft.com")
    for name, value in cookies.items():
        cookie = {"name": name, "value": value}
        driver.add_cookie(cookie)
    return driver


def driver_to_session(driver):
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session
