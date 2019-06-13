from lxml import etree
from PIL import Image
from time import sleep
import requests
import shutil
import json
from tixcraft.picker import AreaPicker
from tixcraft.verify import Verifier
from tixcraft import parser


class NoLoggingError(RuntimeError):
    pass


class ActivityIndexError(RuntimeError):
    pass


class SoldOutError(RuntimeError):
    pass


class PaymentError(RuntimeError):
    pass


class UndefinedUrlError(RuntimeError):
    pass


class TixCraft:
    def __init__(self, activity_url, driver, cookies, **setting):
        self.ACTIVITY_URL = activity_url
        self.driver = driver
        self.ACTIVITY_INDEX = setting.get("activity_index", 0)
        self.TICKET_NUMBER = setting.get("ticket_number", 1)
        self.AREA_NAME = setting.get("area_name", "")
        self.AREA_PRICE = setting.get("area_price", 0)
        self.RULE = setting.get("rule", "")
        self.session = requests.Session()
        self._load_cookies(cookies)

    def _load_cookies(self, cookies):
        for cookie in cookies:
            self.session.cookies.set(cookie["name"], cookie["value"])

    def _is_lang_zh_tw(self):
        cookies = self.session.cookies.get_dict()
        return "zh_tw" in cookies["lang"]

    def _set_lang_zh_tw(self):
        r = requests.get("https://tixcraft.com/user/changeLanguage/lang/zh_tw")
        cookies = r.cookies.get_dict()
        self.session.cookies.update({"lang": cookies["lang"]})

    def get_username(self):
        r = self.session.get("https://tixcraft.com")
        html = etree.HTML(r.text)
        username = html.xpath('//a[@class="user-name"]/text()')
        if not username:
            raise NoLoggingError("尚未登入tixCraft")
        return username[0]

    def activity_detail(self, url):
        url = url.replace("detail", "game")
        return url

    def activity_game(self, url, source_code):
        html = etree.HTML(source_code)
        try:
            td = html.xpath('//td[@class="gridc"]')[self.ACTIVITY_INDEX]
        except IndexError:
            raise ActivityIndexError("活動場次索引不存在")

        status = etree.tostring(td, encoding="unicode")
        if "已售完" in status or "選購一空" in status:
            raise SoldOutError("活動場次已售完")
        elif "立即訂購" in status:
            url = td.xpath("input/@data-href")[0]
            url = "https://tixcraft.com" + url
        elif "剩餘" in status:
            pass

        return url

    def ticket_verify(self, url, source_code):
        verifier = Verifier(self.session, source_code)
        url = verifier.run(self.driver, url)
        return url

    def ticket_area(self, source_code, rule="highest"):
        areas, price_status = parser.areas(source_code)
        areaUrlList = parser.areaUrlList(source_code)

        area_setting = {
            "AREA_NAME": self.AREA_NAME,
            "AREA_PRICE": self.AREA_PRICE,
            "RULE": self.RULE,
        }
        picker = AreaPicker(areas, areaUrlList, **area_setting)
        url = picker.pick_area()
        return "https://tixcraft.com" + url

    def show_captcha(self):
        r = self.session.get("https://tixcraft.com/ticket/captcha", stream=True)
        if r.status_code == 200:
            with open("captcha.png", "wb") as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

            image = Image.open("captcha.png")
            image.show()

    def ticket_ticket(self, url, source_code):
        self.show_captcha()
        CSRFTOKEN = parser.CSRFTOKEN(source_code)
        ticketPrice = parser.ticketPrice(source_code)
        verifyCode = input("請輸入驗證碼: ")
        agree = parser.agree(source_code)

        ticket_number = self.TICKET_NUMBER
        optional_number = parser.optional_number(source_code)

        if ticket_number > optional_number:
            ticket_number = optional_number
            print(f"剩餘可選{optional_number}張")

        ticket_number = str(ticket_number)

        data = {
            "CSRFTOKEN": CSRFTOKEN,
            ticketPrice: ticket_number,
            "TicketForm[verifyCode]": verifyCode,
            agree: "1",
            "ticketPriceSubmit": "",
        }
        return url, data

    def ticket_order(self):
        return "https://tixcraft.com/ticket/check"

    def ticket_check(self, url, source_code):
        json_data = json.loads(source_code)
        message = json_data["message"]
        time = int(json_data["time"])

        if time == 0:
            url = parser.location_replace(message)
            url = "https://tixcraft.com" + url
        else:
            print(f"請等待: {time}秒")
            sleep(time)
        return url

    def ticket_payment(self, source_code):
        if "訂購確認" in source_code:
            url = ""
            return url
        raise PaymentError("PaymentError")

    def request(self, url, data=None):
        if data is None:
            r = self.session.get(url)
        else:
            r = self.session.post(url, data=data)
        return r.url, r.text

    def next_step(self, url, source_code):
        data = None
        if "activity/detail" in url:
            url = self.activity_detail(url)
        elif "activity/game" in url:
            url = self.activity_game(url, source_code)
        elif "ticket/verify" in url:
            url = self.ticket_verify(url, source_code)
        elif "ticket/area" in url:
            url = self.ticket_area(source_code)
        elif "ticket/ticket" in url:
            url, data = self.ticket_ticket(url, source_code)
        elif "ticket/order" in url:
            url = self.ticket_order()
        elif "ticket/check" in url:
            url = self.ticket_check(url, source_code)
        elif "ticket/payment" in url:
            url = self.ticket_payment(source_code)
        else:
            raise UndefinedUrlError("未定義Url: " + url)

        if url != "":
            url, source_code = self.request(url, data)
        # print(url)
        return url, source_code

    def run(self):

        url = self.ACTIVITY_URL
        source_code = ""

        if not self._is_lang_zh_tw():
            self._set_lang_zh_tw()

        try:
            username = self.get_username()
            print("會員:" + username)

            while True:
                url, source_code = self.next_step(url, source_code)
                if url == "":
                    break
            print("Good")
        except RuntimeError as e:
            print(e)
            print("QQ")
