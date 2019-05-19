from tixcraft import func

ACTIVITY_URL = ""
ACTIVITY_INDEX = 0
TICKET_NUMBER = 1
AREA_NAME = ""
AREA_PRICE = 0
RULE = ""


def set_config(activity_url, **setting):
    global ACTIVITY_URL
    global ACTIVITY_INDEX
    global TICKET_NUMBER
    global AREA_NAME
    global AREA_PRICE
    global RULE

    ACTIVITY_URL = activity_url
    ACTIVITY_INDEX = setting.get("activity_index", 0)
    TICKET_NUMBER = setting.get("ticket_number", 1)
    AREA_NAME = setting.get("area_name", "")
    AREA_PRICE = setting.get("area_price", 0)
    RULE = setting.get("rule", func.RANDOM)

    if AREA_NAME != "":
        RULE = func.specific_name_area
    elif AREA_PRICE != 0 and AREA_PRICE > 0:
        RULE = func.specific_price_area
