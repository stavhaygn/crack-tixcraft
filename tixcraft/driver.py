from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


def login(driver):
    driver.implicitly_wait(20)
    driver.get("https://tixcraft.com/login")
    WebDriverWait(driver, 600).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@class='user-name']"))
    )
    cookies = driver.get_cookies()
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
