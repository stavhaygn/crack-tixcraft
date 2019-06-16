Crack-tixCraft 
===
[![](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
[![](https://img.shields.io/github/license/stavhaygn/crack-tixcraft.svg)](https://github.com/stavhaygn/crack-tixcraft/blob/master/LICENSE)
<br>
Tixcraft自動購票系統，實作verify選擇題猜測，驗證碼辨識。

使用說明
---
-url 欲自動購票的活動網址<br>
```
$ python crack_tixcraft.py -url https://tixcraft.com/activity/detail/19_Ann
Using TensorFlow backend.
會員: [G+] [測試員]
辨識驗證碼: twai
請等待: 5秒
Good
```

### 命令列參數

```
$ python crack_tixcraft.py -h
Using TensorFlow backend.
usage: crack_tixcraft.py [-h] -url ACTIVITY_URL [-i ACTIVITY_INDEX]
                         [-n TICKET_NUMBER] [-an AREA_NAME] [-ap AREA_PRICE]
                         [-r RULE]

optional arguments:
  -h, --help         show this help message and exit
  -url ACTIVITY_URL  活動URL (例如 "https://tixcraft.com/activity/detail/19_Ann")
  -i ACTIVITY_INDEX  活動場次索引 (預設 "0")
  -n TICKET_NUMBER   購買票數 (預設 "1")
  -an AREA_NAME      區域名稱 (例如 "藍203")
  -ap AREA_PRICE     區域售價 (例如 "2880")
  -r RULE            區域選取規則 ("hp" 選擇最高售價區域 | "lp" 選擇最低售價區域)
```

環境需求
---
Python3.6、[ChromeDriver](http://chromedriver.chromium.org/)

License
---
[MIT License](https://github.com/stavhaygn/crack-tixcraft/blob/master/LICENSE)