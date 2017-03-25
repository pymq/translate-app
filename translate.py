import configparser
import requests

from googletrans import Translator as gtr


class Translator:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ya_translate = config['DEFAULT']["ya_translate"]
        return

    def translate_google(self, text, dest='ru'):
        translator = gtr()
        res = translator.translate(text, dest=dest)
        return res.text

    def translate_yandex(self, text, dest='en-ru'):
        url = r'https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}'.\
            format(self.ya_translate, text, dest)
        return dict(requests.get(url).json())['text'][0]
