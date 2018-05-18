import re

import requests
from bs4 import BeautifulSoup


class MultitranError(Exception):
    pass


def getTranslationsTable(soup):
    """Returns the translations table from Multitran page, as an element in the list"""
    table = [i for i in soup.find_all('table') if
             not i.has_attr('class') and not i.has_attr('id') and not i.has_attr('width') and i.has_attr(
                 'cellpadding') and i.has_attr('cellspacing') and i.has_attr('border')
             and not len(i.find_all('table'))]
    return table


def getReplacementVariants(soup):
    varia = soup.find_all('td', string=re.compile("Варианты"))
    variants_list = []
    if varia:
        variants_list = [i for i in varia[0].find_next_sibling("td").text.split(";")]
    return variants_list


def processTable(table, links_on=False):
    result = ""
    words_list = []
    word_index = 0

    def translations_row(word_index):
        _result = '\t\t' + tr.find_all('a')[0].text + "- "
        _words_list = []
        for a in tr.find_all('a')[1:]:
            if not 'i' in [i.name for i in a.children]:
                i_word = a.text.strip(" \n\t\r")
                # print(3, i_word)
                if i_word == "в начало":
                    break
                a_word = i_word + ", "
                _words_list += [i_word]
                # add a word, checking if a user wants links
                _result += a_word if not links_on else ("/" + str(word_index) + " " + a_word + "\n")
                word_index += 1
        return _result, word_index, _words_list

    for tr in table.find_all('tr'):
        # for each row, corresponds to topic
        tds = tr.find_all('td')

        if tds[0].has_attr('bgcolor') and tds[0]['bgcolor'] == "#DBDBDB":
            # a header of the table, with initial word and its properties
            result += "\n" + "" + tr.text.split("|")[0].replace(
                tr.find_all('em')[0].text if tr.find_all('em') else "", "").replace("в начало", "").replace("фразы",
                                                                                                            "").replace(
                "\n", "") + "" + (
                          (" " + "(" + tr.find_all('em')[0].text + ")") if tr.find_all('em') else "")
        else:
            r, word_index, word_list_fraction = translations_row(word_index)
            words_list += word_list_fraction
            result += r
        result += "\n"

    return result.strip(), words_list


def dictQuery(request, lang, links_on=False):
    """
    :param request: a word to search
    :param lang: index of a foreign language
    :param links_on: should the links be present in the reply or not?
    :return: a tuple. First element is always a signal.
    0 - Normal.
    1 - Could not connect to Multitran.
    2 - Word not found.
    """
    soup = None
    page_url = ""
    for russian in range(2):
        # try a foreign language in first iteration, and if not found, try Russian in second one.
        try:
            status_code, page, page_url = getMultitranPage(request, lang, from_russian=bool(russian))
        except MultitranError:
            return 1

        soup = BeautifulSoup(page, "lxml")

        translations_table = getTranslationsTable(soup)
        if translations_table:
            # word is found continue to processing
            # have to extract translations_table[0] from list
            result, words_list = processTable(translations_table[0], links_on)
            return 0, result, page_url, words_list
    else:
        # word not found. Process possible variants
        variants = getReplacementVariants(soup)
        if variants:
            return 2, variants, page_url
        else:
            return 2, [], page_url


def getMultitranPage(word, lang, from_russian=False, attempts=3):
    """Processes the Multitran page. Returns the status code and content."""

    # escape the word in URL.
    try:
        word_escaped = requests.utils.quote(word.encode("cp1251"))
    except UnicodeEncodeError:
        word_escaped = requests.utils.quote(word.encode('utf-8', 'replace'))

    if from_russian:
        page_url = 'http://www.multitran.ru/c/m.exe?l1=2&l2={0}&s={1}'.format(lang, word_escaped)
    else:
        page_url = 'http://www.multitran.ru/c/m.exe?l1={0}&s={1}'.format(lang, word_escaped)

    MULTITRAN_ERROR_TEXT = 'Multitran is down!'

    for i in range(attempts):
        try:
            req = requests.get(page_url)
        except:
            raise MultitranError(MULTITRAN_ERROR_TEXT)
        if req.status_code == 200:
            break
    else:
        raise MultitranError(MULTITRAN_ERROR_TEXT)

    return req.status_code, req.content.decode("cp1251", "replace"), page_url


def translate(word, lang=1):  # TODO rename
    result = dictQuery(word, lang)
    if result == 1:
        return 'Error'
    else:
        reply = ''
        if isinstance(result, tuple):
            if result[0] == 0:
                reply += result[1]

            elif result[0] == 2:
                # Word not found. Replacements may be present
                variants = result[1]
                variants[0] = ' ' + variants[0]  # add space to first variant

                string_variants = "Suggestions:\n"
                for n, variant in enumerate(variants):
                    string_variants += str(n + 1) + "." + variant + "\n"
                reply = string_variants
            return reply
