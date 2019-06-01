from selenium import webdriver
from argparse import ArgumentParser
import json
from tixcraft.core import TixCraft
from tixcraft.driver import login
from tixcraft.picker import AreaPicker


def get_args():

    parser = ArgumentParser()
    parser.add_argument(
        "-url",
        help="activity url, such as https://tixcraft.com/activity/detail/19_Ann",
        dest="activity_url",
        required=True,
    )
    parser.add_argument(
        "-i",
        help='activity index (default "0")',
        dest="activity_index",
        default=0,
        type=int,
    )
    parser.add_argument(
        "-n",
        help='ticket number (default "1")',
        dest="ticket_number",
        default=1,
        type=int,
    )
    parser.add_argument("-an", help="area name", dest="area_name", default="")
    parser.add_argument(
        "-ap", help="area price", dest="area_price", default=0, type=int
    )
    parser.add_argument("-r", help="pick area rule", dest="rule", default="")
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
    tixcraft = TixCraft(activity_url, cookies, **setting)
    tixcraft.run()


if __name__ == "__main__":
    main()
