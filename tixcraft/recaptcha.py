from keras.models import load_model
import tensorflow as tf
from PIL import Image
import numpy as np

tf.logging.set_verbosity(tf.logging.ERROR)

try:
    char_model = load_model("./models/Reenie_Beanie_model.h5")
except OSError:
    char_model = None


class Recaptcha:
    def __init__(self, session):
        self.session = session
        self.captcha_image = self._save_captcha()

    def _save_captcha(self):
        r = self.session.get("https://tixcraft.com/ticket/captcha", stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            captcha_image = Image.open(r.raw)
            return captcha_image

    def _data(self):
        data = np.array(self.captcha_image.convert("L")).astype("float16") / 255
        data = np.array([data])
        data = data.reshape(data.shape + (1,))
        return data

    def _predict_captcha(self, data):
        evaluates = char_model.predict(data)
        indexes = [evaluate.argmax() for evaluate in evaluates]
        captcha = "".join([chr(index + 0x61) for index in indexes])
        return captcha

    def _user_input(self):
        self.captcha_image.show()
        captcha = input("請輸入驗證碼: ")
        return captcha

    def run(self):
        if char_model is not None:
            data = self._data()
            captcha = self._predict_captcha(data)
            print("辨識驗證碼:", captcha)
        else:
            captcha = self._user_input()
        return captcha
