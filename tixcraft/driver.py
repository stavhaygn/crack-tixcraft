from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from lxml import etree
from tixcraft import parser


def login(driver):
    driver.implicitly_wait(20)
    driver.get("https://tixcraft.com/login")
    WebDriverWait(driver, 600).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@class='user-name']"))
    )
    cookies = driver.get_cookies()
    return cookies


class Verifier:
    def __init__(self, driver, session, url, source_code):
        self.driver = driver
        self.session = session
        self.url = url
        self.html = etree.HTML(source_code)
        self.CSRFTOKEN = parser.CSRFTOKEN(self.html)
        self.checkcode_url = parser.checkcode_url(source_code)

    def _verify(self, checkCode):
        data = {
            "CSRFTOKEN": self.CSRFTOKEN,
            "checkCode": checkCode,
            "confirmed": "true",
        }
        r = self.session.post(self.checkcode_url, data=data)
        url = parser.json_url(r.text)
        return "https://tixcraft.com" + url

    def _undefined(self):
        print(self.url)
        self.driver.get(self.url)
        url = self.driver.current_url
        while "ticket/verify" in url:
            try:
                url = self.driver.current_url
                WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert = self.driver.switch_to_alert()
                alert.accept()
            except:
                pass
        return url

    def _choice(self):
        div = self.html.xpath("//form/div[1]/div[1]")[0]
        div = etree.tostring(div, encoding="unicode")
        if "Q1" in div and "Q2" in div:
            url = self._muti_choice()
        else:
            url = self._single_choice()
        return url

    def _single_choice(self):
        url = ""
        return url

    def _muti_choice(self):
        url = ""
        return url

    def _copy_paste(self):
        url = ""
        try:
            checkcode = self.html.xpath("//font/text()")[-1]
            url = self._verify(checkcode)
        except IndexError:
            pass
        return url

    def run(self):
        url = self._copy_paste()
        if url:
            return url
        url = self._undefined()
        return url
