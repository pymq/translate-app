import configparser
import requests
import json

from googletrans import Translator as gtr
from vocabulary.vocabulary import Vocabulary as voc


class Translator:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ya_translate_token = config['Yandex']["translate_token"]
        self.ya_dictionary_token = config['Yandex']["dictionary_token"]
        # self.abbyy_key = config['Lingvolive_ABBYY']["key"]
        # self.abbyy_token = ''
        # self.abbyy_get_token(self.abbyy_key)

    def translate_google(self, text, lang='en-ru'):
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

    def abbyy_get_token(self, abbyy_key):
        # token TTL 24h
        url = r'https://developers.lingvolive.com/api/v1.1/authenticate'
        headers = dict(Authorization="Basic " + abbyy_key)
        response = requests.post(url, headers=headers)
        self.abbyy_token = response.text

    def synonym(self, text):
        # do not support russian
        response = voc.synonym(text)
        if not response or response == '[]':
            return ''
        response = json.loads(response)
        output = "Synonyms:\n"
        i = 1
        for a in response:
            output += '\t' + str(i) + '. ' + a['text']
            output += '\n'
            i += 1
        return output

    def definition(self, text):
        # do not support russian
        response = voc.meaning(text)
        if not response or response == '[]':
            return ''
        response = json.loads(response)
        output = "Definitions:\n"
        i = 1
        for a in response:
            output += '\t' + str(i) + '. ' + a['text']
            output += '\n'
            i += 1
        return output

    def translate_yandex(self, text, lang='en-ru'):
        url = r'https://translate.yandex.net/api/v1.5/tr.json/translate'
        payload = dict(key=self.ya_translate_token, text=text, lang=lang)
        return dict(requests.get(url, payload).json())['text'][0]

    def dictionary_yandex(self, text, lang='en-ru'):
        url = r'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
        payload = dict(key=self.ya_dictionary_token, text=text, lang=lang, ui='ru')
        response = dict(requests.get(url, payload).json())['def']
        result = ''
        for pos in response:
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
        return result.strip()
