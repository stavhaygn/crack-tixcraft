import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from keras.models import load_model
from PIL import Image
import numpy as np


try:
    font_model = load_model("./models/Font_model.h5", compile=False)
    Reenie_model = load_model("./models/Reenie_Beanie_model.h5", compile=False)
except OSError:
    font_model = None
    Reenie_model = None

Reenie_Beanie = "Reenie_Beanie"
Gloria_Hallelujah = "Gloria_Hallelujah"
Covered_By_Your_Grace = "Covered_By_Your_Grace"

FONT_DECODE = [Covered_By_Your_Grace, Gloria_Hallelujah, Reenie_Beanie]


class Recaptcha:
    def __init__(self, session):
        self.session = session

    def _captcha_image(self):
        r = self.session.get("https://tixcraft.com/ticket/captcha", stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            captcha_image = Image.open(r.raw)
            return captcha_image

    def _data(self, image, turn_color=True):
        data = np.array(image.convert("L")).astype("float16") / 255
        if turn_color:
            data = 1 - data
        data = np.array([data])
        data = data.reshape(data.shape + (1,))
        return data

    def _recognize_font(self, data):
        evaluate = font_model.predict(data)
        font = FONT_DECODE[evaluate.argmax()]
        return font

    def _recognize_captcha(self, char_model, data):
        evaluates = char_model.predict(data)
        indexes = [evaluate.argmax() for evaluate in evaluates]
        captcha = "".join([chr(index + 0x61) for index in indexes])
        return captcha

    def _recognize(self):
        font = None
        captcha_image = None
        times = 0
        while font != Reenie_Beanie:
            if times == 5:
                self.session.get("https://tixcraft.com/ticket/captcha?refresh=1")
                times = 0
            captcha_image = self._captcha_image()
            data = self._data(captcha_image)
            font = self._recognize_font(data)
            times += 1

        data = self._data(captcha_image, turn_color=False)
        captcha = self._recognize_captcha(Reenie_model, data)
        return captcha

    def _user_input(self):
        captcha_image = self._captcha_image()
        captcha_image.show()
        captcha = input("請輸入驗證碼: ")
        return captcha

    def run(self):
        if font_model is not None and Reenie_model is not None:
            captcha = self._recognize()
            print("辨識驗證碼:", captcha)
        else:
            captcha = self._user_input()
        return captcha
