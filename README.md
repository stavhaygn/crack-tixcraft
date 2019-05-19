Crack-tixCraft
===
Automatically buy tickets.

Usage
---

### From module

```python=
from tixcraft.core import run

setting = {
        "activity_index": activity_index,
        "ticket_number": ticket_number,
        "area_name": area_name,
        "area_price": area_price,
        "rule": rule,
}

run("https://tixcraft.com/activity/detail/19_Ann", setting)
```

### Command line usage

If there isn't `session.json` in directory, follow below steps.
The first, modify email and passwd variable in `secret.py`,
and the second, run `login_tixcraft.py` to login tixcraft and save the session.json.
```
$ python login_tixcraft.py
```

Finally, you have `session.json`, and then run `crack_tixcraft.py`
```
$ python crack_tixcraft.py -url https://tixcraft.com/activity/detail/19_Ann
會員: [G+] [測試員]
請輸入驗證碼: fevo
請等待: 5秒
Good
```

### Command line options

```
$ python crack_tixcraft.py -h
usage: crack_tixcraft.py [-h] -url ACTIVITY_URL [-i ACTIVITY_INDEX]
                         [-n TICKET_NUMBER] [-an AREA_NAME] [-ap AREA_PRICE]
                         [-r RULE]

optional arguments:
  -h, --help         show this help message and exit
  -url ACTIVITY_URL  activity url, such as
                     https://tixcraft.com/activity/detail/19_Ann
  -i ACTIVITY_INDEX  activity index (default "0")
  -n TICKET_NUMBER   ticket number (default "1")
  -an AREA_NAME      area name
  -ap AREA_PRICE     area price
  -r RULE            pick area rule
```

Requirements
---
You need Python 3.6 or later to run crack-tixcraft.

License
---
MIT License