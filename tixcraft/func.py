import random
from tixcraft import config


def is_onsale(area_status):
    return "剩餘" in area_status or "熱賣中" in area_status


def specific_name_area(areas):
    picked_area_id = None
    for area_id, area_info in areas.items():
        area_name = area_info[0]
        if config.AREA_NAME in area_name:
            picked_area_id = area_id
    return picked_area_id


def specific_price_area(areas):
    picked_area_id = None
    for area_id, area_info in areas.items():
        area_price = area_info[1]
        if config.AREA_PRICE == area_price:
            picked_area_id = area_id
            break
    return picked_area_id


def highest_price_area(areas):
    highest_price = 0
    picked_area_id = None
    for area_id, area_info in areas.items():
        _, area_price, area_status = area_info
        if is_onsale(area_status):
            if area_price > highest_price:
                highest_price = area_price
                picked_area_id = area_id
    return picked_area_id


def lowest_price_area(areas):
    lowest_price = 99999
    picked_area_id = None
    for area_id, area_info in areas.items():
        _, area_price, area_status = area_info
        if is_onsale(area_status):
            if area_price < lowest_price:
                lowest_price = area_price
                picked_area_id = area_id
    return picked_area_id


def random_area(areas):
    areas_id = list(areas.keys())
    rand = random.randint(0, len(areas_id) - 1)
    picked_area_id = areas_id[rand]
    return picked_area_id


SPECIFIC_NAME = "SPECIFIC_NAME"
SPECIFIC_PRICE = "SPECIFIC_PRICE"
HIGHEST_PRICE = "HIGHEST_PRICE"
LOWEST_PRICE = "LOWEST_PRICE"
RANDOM = "RANDOM"

pick_funcs = {
    "SPECIFIC_NAME": specific_name_area,
    "SPECIFIC_PRICE": specific_price_area,
    "HIGHEST_PRICE": highest_price_area,
    "LOWEST_PRICE": lowest_price_area,
    "RANDOM": random_area,
}
