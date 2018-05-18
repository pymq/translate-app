# Description
Hardcoded en-ru & ru-en translation.

# Hotkeys
- arrows up & down - перемещение по истории
- Enter OR Ctrl + Space - перевод
- Ctrl + Q - свернуть окно
- Ctrl + Shift + Q - закрыть окно
- Ctrl + L - перемещение курсора на ввод

# Features:
- перевод от Гугла
- перевод, словарь Яндекса
- определения от urbandictionary, wordnik, glosbe, bighugelabs, multitran
- автоматическое определение направления перевода
- SystemTrayIcon
- сохранение истории перевода в файл и возможность просмотра истории с помощью стрелок вверх и вниз
- хранение результатов на время запуска
- подсказки при вводе по списку слов и выражений из файла `dictionary.txt`. Словарь русских и английских слов можно взять [отсюда](https://raw.githubusercontent.com/pymq/dictionaries/master/dictionary.txt)

# Installation
Для использования Яндекс словаря и Яндекс переводчика необходимо получить бесплатный API ключ [здесь](https://tech.yandex.ru/translate/doc/dg/concepts/api-keys-docpage/) и [здесь](https://tech.yandex.ru/keys/get/?service=dict) и создать в папке файл `config.ini` со следующим содержимым:
```
[Yandex]
translate_token = trnsl.1.1.xxxxxxxxx.xxxxxxxxx.xxxxxxxxxxxxx
dictionary_token = dict.1.1.xxxxxxxxx.xxxxxxxxx.xxxxxxxxxxxxx
```
Простой запуск:
```
pip install -r requirements.txt
python window.py
```
Можно собрать с помощью PyInstaller:
```
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconsole --icon icon.png --name translator window.py
```
Тогда в подпапке `dist/translator` будет находиться исполняемый файл `translator`
