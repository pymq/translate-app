import configparser
import json

import requests
from googletrans import Translator as gtr
from vocabulary.vocabulary import Vocabulary as voc

from multitran import translate


class Translator:
    def __init__(self, config_path):
        """
        :param config_path: путь до файла с конфигурацией
        """
        config = configparser.ConfigParser()
        config.read(config_path)
        self.ya_translate_token = config.get('Yandex', 'translate_token')
        self.ya_dictionary_token = config.get('Yandex', 'dictionary_token')
        # self.abbyy_key = config['Lingvolive_ABBYY']["key"]
        # self.abbyy_token = self._abbyy_get_token(self.abbyy_key)

    @staticmethod
    def translate_google(text, lang='en-ru'):
        src, dest = lang.split('-')
        translator = gtr()
        res = translator.translate(text, dest=dest, src=src)
        return res.text

    def abbyy_translate(self, text, lang):
        # (En-En) 1033→1031
        # API?: Suggests, Minicard, WordList
        url = r'https://developers.lingvolive.com/api/v1/Translation'
        headers = {'Authorization': 'Bearer ' + self.abbyy_token}
        lang = lang.replace('en', '1033')
        lang = lang.replace('ru', '1049')
        src, dest = lang.split('-')
        # params = dict(text=text, srcLang=src, dstLang=dest)
        params = {'text': text, 'srcLang': src, 'dstLang': dest}
        response = requests.get(url, params=params, headers=headers)
        response = json.loads(response.text)
        res = ''
        for dict in response:
            res += dict['Dictionary']
            res += '\n'

    def _abbyy_get_token(self, abbyy_key):
        # token TTL 24h
        url = r'https://developers.lingvolive.com/api/v1.1/authenticate'
        headers = dict(Authorization="Basic " + abbyy_key)
        response = requests.post(url, headers=headers)
        return response.text

    def translate_multitran(self, text, lang):
        lang = 1  # TODO
        return translate(text, lang)

    @staticmethod
    def synonym(text, lang='en-en'):
        # do not support russian
        src, dest = lang.split('-')
        response = voc.synonym(text, src, dest)
        if not response or response == '[]':
            return ''
        response = json.loads(response)
        output = ""
        for i, a in enumerate(response, start=1):
            output += '\t' + str(i) + '. ' + a['text']
            output += '\n'
        return output

    @staticmethod
    def definition(text, lang='en-en'):
        # do not support russian
        src, dest = lang.split('-')
        response = voc.meaning(text, src, dest)
        if not response or response == '[]':
            return ''
        response = json.loads(response)
        output = ""
        for i, a in enumerate(response, start=1):
            output += '\t' + str(i) + '. ' + a['text']
            output += '\n'
        return output

    def translate_yandex(self, text, lang='en-ru'):
        url = r'https://translate.yandex.net/api/v1.5/tr.json/translate'
        payload = dict(key=self.ya_translate_token, text=text, lang=lang)
        return dict(requests.get(url, payload).json())['text'][0]

    def dictionary_yandex(self, text, lang='en-ru'):
        url = r'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
        payload = dict(key=self.ya_dictionary_token, text=text, lang=lang, ui='ru')
        response = dict(requests.get(url, payload).json()).get('def')
        if not response:
            return ''
        result = ''
        for pos in response:
            if 'pos' in pos and 'text' in pos:
                result = result + pos['pos'] + ' ' + pos['text'] + ' - '
            for i, variant in enumerate(pos['tr'], start=1):
                tr_syn_list = []
                en_syn_list = []
                tr_syn_list.append(variant['text'])
                result = result + '\n\t' + str(i) + '. '
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
        return result.strip()
