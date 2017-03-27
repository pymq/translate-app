#!/home/max/DesktopTranslator/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from translate import Translator


class Handler:
    def __init__(self):
        self.lang = 'en-ru'
        return

    def on_entry_enter_press_event(self, *args): #TODO: рассмотреть вариант поиска по Ctrl + space
        input_text = entry.get_text()
        # translate
        #TODO: автоматическое распознавание языка перевода
        #TODO: unit-тесты
        #TODO: вывод перевода по мере загрузки
        tr = Translator()
        # when ru-en it throws HTTP 403 err
        if self.lang == 'ru-en':
            buffer1.set_text('')
        elif self.lang == 'en-ru':
            buffer1.set_text(tr.translate_google(input_text,self.lang) + '\n\n\n\nGoogle Translate')

        buffer2.set_text(tr.translate_yandex(input_text, self.lang) + '\n\n\n\nYandex Translate')
        buffer3.set_text(tr.dictionary_yandex(input_text, self.lang) + '\n\n\n\nYandex Dictionary')

    def onWindowDestroy(self, *args):
        gtk.main_quit()

    #TODO: switcher
    def on_switch_state_set(self,switch,state):
        if state:
            self.lang = 'ru-en'
        else:
            self.lang = 'en-ru'


builder = gtk.Builder()
builder.add_from_file("mainwindow.glade")

window = builder.get_object('window')
window.set_title('Desktop translator')
entry = builder.get_object('entry')
switcher = builder.get_object('switch')
textview1 = builder.get_object('textview1')
textview2 = builder.get_object('textview2')
textview3 = builder.get_object('textview3')

builder.connect_signals(Handler())

buffer1 = gtk.TextBuffer()
buffer2 = gtk.TextBuffer()
buffer3 = gtk.TextBuffer()

textview1.set_buffer(buffer1)
textview2.set_buffer(buffer2)
textview3.set_buffer(buffer3)

window.show_all()
gtk.main()
