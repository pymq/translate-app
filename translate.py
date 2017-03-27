import configparser
import requests

from googletrans import Translator as gtr


class Translator:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ya_translate_token = config['DEFAULT']["ya_translate_token"]
        self.ya_dictionary_token = config['DEFAULT']["ya_dictionary_token"]
        return

    def translate_google(self, text, dest='ru'):
        translator = gtr()
        res = translator.translate(text, dest=dest)
        return res.text

    #TODO: summary
    def translate_yandex(self, text, dest='en-ru'):
        url = r'https://translate.yandex.net/api/v1.5/tr.json/translate'
        payload = dict(key=self.ya_translate_token, text=text, lang=dest)
        return dict(requests.get(url, payload).json())['text'][0]

    def dictionary_yandex(self, text, dest='en-ru'):
        url = r'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
        payload = dict(key=self.ya_dictionary_token, text=text, lang=dest, ui='ru')
        api_answer = dict(requests.get(url, payload).json())['def']
        result = ''
        for pos in api_answer:
            result = result + pos['pos'] + ' ' + pos['text'] + ' - '
            i = 1
            for variant in pos['tr']:
                tr_syn_list = []
                en_syn_list = []
                tr_syn_list.append(variant['text'])
                result = result + '\n\t' + str(i) + '. '
                i += 1
                if 'syn' in variant:
                    for syn in variant['syn']:
                        tr_syn_list.append(syn['text'])
                if 'mean' in variant:
                    for mean in variant['mean']:
                        en_syn_list.append(mean['text'])
                result = result + ', '.join(tr_syn_list)
                if len(en_syn_list) != 0:
                    result = result + '\n\t   ' + '(' + ', '.join(en_syn_list) + ')'
            result = result + '\n\n'
        return result
