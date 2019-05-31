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
