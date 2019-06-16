from argparse import ArgumentParser
from selenium import webdriver
import json
from tixcraft.picker import AreaPicker
from tixcraft.core import TixCraft
from tixcraft.driver import login


def get_args():

    parser = ArgumentParser()
    parser.add_argument(
        "-url",
        help='活動URL (例如 "https://tixcraft.com/activity/detail/19_Ann")',
        dest="activity_url",
        required=True,
    )
    parser.add_argument(
        "-i", help='活動場次索引 (預設 "0")', dest="activity_index", default=0, type=int
    )
    parser.add_argument(
        "-n", help='購買票數 (預設 "1")', dest="ticket_number", default=1, type=int
    )
    parser.add_argument("-an", help='區域名稱 (例如 "藍203")', dest="area_name", default="")
    parser.add_argument(
        "-ap", help='區域售價 (例如 "2880")', dest="area_price", default=0, type=int
    )
    parser.add_argument(
        "-r", help='區域選取規則 ("hp" 選擇最高售價區域 | "lp" 選擇最低售價區域)', dest="rule", default=""
    )
    return parser.parse_args()


def convert_rule(rule):
    rules = {
        "hp": AreaPicker.HIGHEST_PRICE,
        "lp": AreaPicker.LOWEST_PRICE,
        "r": AreaPicker.RANDOM,
        "sn": AreaPicker.SPECIFIC_NAME,
        "sp": AreaPicker.SPECIFIC_PRICE,
    }
    try:
        rule = rules[rule]
    except KeyError:
        rule = AreaPicker.RANDOM
    return rule


def main():
    args = get_args()

    activity_url = args.activity_url
    setting = {
        "activity_index": args.activity_index,
        "ticket_number": args.ticket_number,
        "area_name": args.area_name,
        "area_price": args.area_price,
        "rule": convert_rule(args.rule),
    }

    driver = webdriver.Chrome()
    cookies = login(driver)
    tixcraft = TixCraft(activity_url, driver, cookies, **setting)
    tixcraft.run()


if __name__ == "__main__":
    main()
