from argparse import ArgumentParser
from tixcraft.core import run
from tixcraft import func


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
    parser.add_argument("-r", help="pick area rule", dest="rule", default=func.RANDOM)
    return parser.parse_args()


def convert_rule(rule):
    rules = {
        "hp": func.HIGHEST_PRICE,
        "lp": func.LOWEST_PRICE,
        "r": func.RANDOM,
        "sn": func.SPECIFIC_NAME,
        "sp": func.SPECIFIC_PRICE,
    }
    try:
        rule = rules[rule]
    except KeyError:
        rule = func.RANDOM
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

    run(activity_url, setting)


if __name__ == "__main__":
    main()
