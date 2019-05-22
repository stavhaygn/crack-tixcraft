from lxml import etree
from PIL import Image
from time import sleep
import requests
import shutil
import json
from tixcraft import config, parser
from tixcraft.func import pick_funcs


session = requests.Session()


class SessionFileNotFoundError(RuntimeError):
    pass


class NoLoggingError(RuntimeError):
    pass


class ActivityIndexError(RuntimeError):
    pass


class PaymentError(RuntimeError):
    pass


class UndefinedUrlError(RuntimeError):
    pass


def load_cookies():
    try:
        with open("session.json") as f:
            cookies = json.load(f)
        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"])
    except FileNotFoundError:
        raise SessionFileNotFoundError("檔案session.json不存在")


def set_lang_zh_tw():
    session.get("https://tixcraft.com/user/changeLanguage/lang/zh_tw")


def get_username():
    r = session.get("https://tixcraft.com")
    html = etree.HTML(r.text)
    username = html.xpath('//a[@class="user-name"]/text()')
    if not username:
        raise NoLoggingError("尚未登入tixCraft")
    return username[0]


def activity_detail(url):
    url = url.replace("detail", "game")
    return url


def activity_game(source_code):
    html = etree.HTML(source_code)
    urls = html.xpath('//td[@class="gridc"]/input/@data-href')
    try:
        url = urls[config.ACTIVITY_INDEX]
    except IndexError:
        raise ActivityIndexError("活動場次索引不存在")

    return "https://tixcraft.com" + url


def ticket_verify(source_code):
    html = etree.HTML(source_code)
    CSRFTOKEN = parser.CSRFTOKEN(html)
    checkCode = parser.checkcode(html)

    data = {"CSRFTOKEN": CSRFTOKEN, "checkCode": checkCode, "confirmed": "true"}
    url = parser.checkcode_url(source_code)
    r = session.post(url, data=data)
    url = parser.json_url(r.text)

    return "https://tixcraft.com" + url


def ticket_area(source_code, rule="highest"):

    areas, price_status = parser.areas(source_code)
    areaUrlList = parser.areaUrlList(source_code)

    rule = config.RULE
    if rule == "HIGHEST" or rule == "LOWEST":
        if price_status == 0:
            rule = "RANDOM"

    picked_area_id = pick_funcs[rule](areas)
    if picked_area_id is None:
        picked_area_id = pick_funcs["RANDOM"](areas)

    url = areaUrlList[picked_area_id]
    return "https://tixcraft.com" + url


def show_captcha():
    r = session.get("https://tixcraft.com/ticket/captcha", stream=True)
    if r.status_code == 200:
        with open("captcha.png", "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        image = Image.open("captcha.png")
        image.show()


def ticket_ticket(url, source_code):
    show_captcha()
    html = etree.HTML(source_code)
    CSRFTOKEN = parser.CSRFTOKEN(html)
    ticketPrice = parser.ticketPrice(html)
    verifyCode = input("請輸入驗證碼: ")
    agree = parser.agree(source_code)

    ticket_number = config.TICKET_NUMBER
    optional_number = parser.optional_number(html)

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


def ticket_order():
    return "https://tixcraft.com/ticket/check"


def ticket_check(url, source_code):
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


def ticket_payment(source_code):
    if "訂購確認" in source_code:
        url = ""
        return url
    raise PaymentError("PaymentError")


def request(url, data=None):
    if data is None:
        r = session.get(url)
    else:
        r = session.post(url, data=data)
    return r.url, r.text


def next_step(url, source_code):
    data = None
    if "activity/detail" in url:
        url = activity_detail(url)
    elif "activity/game" in url:
        url = activity_game(source_code)
    elif "ticket/verify" in url:
        url = ticket_verify(source_code)
    elif "ticket/area" in url:
        url = ticket_area(source_code)
    elif "ticket/ticket" in url:
        url, data = ticket_ticket(url, source_code)
    elif "ticket/order" in url:
        url = ticket_order()
    elif "ticket/check" in url:
        url = ticket_check(url, source_code)
    elif "ticket/payment" in url:
        url = ticket_payment(source_code)
    else:
        UndefinedUrlError("未定義Url: " + url)

    if url != "":
        url, source_code = request(url, data)
    # print(url)
    return url, source_code


def run(activity_url, setting):
    config.set_config(activity_url, **setting)

    url = config.ACTIVITY_URL
    source_code = ""

    try:
        load_cookies()
        set_lang_zh_tw()
        username = get_username()
        print("會員:" + username)

        while True:
            url, source_code = next_step(url, source_code)
            if url == "":
                break
        print("Good")
    except RuntimeError as e:
        print(e)
        print("QQ")
