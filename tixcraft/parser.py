from lxml import etree
import requests
import shutil
import json
import re


class NoFreeAreaError(RuntimeError):
    pass


def CSRFTOKEN(html):
    CSRFTOKEN = html.xpath('//input[@name="CSRFTOKEN"]/@value')[0]
    return CSRFTOKEN


def checkcode(html):
    return html.xpath("//font/text()")[-1]


def checkcode_url(source_code):
    url = re.findall(r"'url':'[^']+", source_code)[-1]
    url = "https://tixcraft.com" + url.split("'")[-1].replace("\\x2F", "/")
    return url


def json_url(source_code):
    return json.loads(source_code)["url"]


def _get_price(area_name):
    price = 0
    try:
        price = int(re.findall(r"\d\d\d+", area_name)[-1])
    except:
        pass
    return price


def areas(source_code):
    html = etree.HTML(source_code)
    areas_id = html.xpath('//div[@class="zone area-list"]/ul/li/a/@id')
    areas_name = html.xpath('//div[@class="zone area-list"]/ul/li/a/text()')
    areas_price = [_get_price(area_name) for area_name in areas_name]
    areas_status = html.xpath('//div[@class="zone area-list"]/ul/li/a/font/text()')
    areas_info = list(zip(areas_name, areas_price, areas_status))
    areas = dict(zip(areas_id, areas_info))

    if not areas_id:
        raise NoFreeAreaError("所有區域已售完")

    price_status = areas_price[0]
    return areas, price_status


def areaUrlList(source_code):
    areaUrlList = re.findall(r"areaUrlList = {[^}]+}", source_code)[0]
    areaUrlList = areaUrlList.replace("\\", "").replace("areaUrlList = ", "")
    areaUrlList = eval(areaUrlList)
    return areaUrlList


def ticketPrice(html):
    ticketPrice = html.xpath('//tr[@class="gridc"]/td/select/@name')[0]
    return ticketPrice


def optional_number(html):
    optional_number = int(html.xpath("//option/@value")[-1])
    return optional_number


def agree(source_code):
    agree = re.findall(r"TicketForm\[agree]\[\S+\]", source_code)[0]
    return agree


def location_replace(message):
    url = re.findall(r"replace\(\"[^\"]+", message)[0][9:]
    return url


def all_activaties_url():
    r = requests.get("https://tixcraft.com/activity")
    html = etree.HTML(r.text)
    names = html.xpath('//div[@id="selling"]/table/tbody/tr/td/a/text()')
    urls = html.xpath('//div[@id="selling"]/table/tbody/tr/td/a/@href')
    urls = ["https://tixcraft.com" + url for url in urls]
    activities = dict(zip(names, urls))
    return activities


def _event_status(td):
    td = etree.tostring(td, encoding="unicode")
    if "已售完" in td or "選購一空" in td:
        return False
    return True


def events(url):
    url = url.replace("detail", "game")
    r = requests.get(url)
    html = etree.HTML(r.text)
    times = html.xpath('//tr[@class="gridc fcTxt"]/td[1]/text()')
    tds = html.xpath('//td[@class="gridc"]')
    statuses = [_event_status(td) for td in tds]
    return times, statuses
