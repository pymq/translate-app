#!/usr/bin/python3

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from translate import Translator


class Handler:
    def __init__(self):
        self.lang = 'en-ru'
        return

    def on_entry_enter_press_event(self, *args):
        input_text = entry.get_text()
        # translate
        # TODO: рассмотреть вариант поиска по Ctrl + space. on_window_delete_event
        # TODO: Entry completion
        # TODO: автоматическое распознавание языка перевода
        # TODO: unit-тесты
        # TODO: вывод перевода по мере загрузки
        # TODO: signal - обработка нажатий
        tr = Translator()
        # when ru-en it throws HTTP 403 err
        if self.lang == 'ru-en':
            buffer1.set_text('')
        elif self.lang == 'en-ru':
            buffer1.set_text(tr.translate_google(input_text, self.lang) + '\n\n\n\nGoogle Translate')

        buffer2.set_text(tr.translate_yandex(input_text, self.lang) + '\n\n\n\nYandex Translate')
        buffer3.set_text(tr.dictionary_yandex(input_text, self.lang) + '\n\n\n\nYandex Dictionary')

    def on_window_delete_event(self, *args):
        window.hide()
        return True

    def on_button_clicked(self, button, *user_data):
        self.on_entry_enter_press_event()

    def on_switch_state_set(self, switch, state):
        if state:
            self.lang = 'ru-en'
        else:
            self.lang = 'en-ru'


class TrayIcon:
    def __init__(self, icon, menu, app_id):
        self.menu = menu

        APPIND_SUPPORT = 1
        try:
            gi.require_version('AppIndicator3', '0.1')
            from gi.repository import AppIndicator3
        except:
            APPIND_SUPPORT = 0

        if APPIND_SUPPORT == 1:
            self.ind = AppIndicator3.Indicator.new(
                app_id, icon,
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.ind.set_menu(self.menu)
        else:  # if AppIndicator3 is unavailable
            self.ind = gtk.StatusIcon()
            self.ind.connect('popup-menu', self.on_popup_menu)

    def on_popup_menu(self, icon, button, time):
        self.menu.popup(None, None, gtk.StatusIcon.position_menu, icon,
                        button, time)


app_id = "Desktop translator"
curr_dir = os.path.dirname(os.path.abspath(__file__))
icon = os.path.join(curr_dir, 'icon.png')
builder = gtk.Builder()
builder.add_from_file("mainwindow.glade")
builder.connect_signals(Handler())

window = builder.get_object('window')
window.set_title('Desktop translator')
entry = builder.get_object('entry')
switcher = builder.get_object('switch')
textview1 = builder.get_object('textview1')
textview2 = builder.get_object('textview2')
textview3 = builder.get_object('textview3')

menu = gtk.Menu()
menuitem_translate = gtk.MenuItem(label='Translate')
menuitem_exit = gtk.MenuItem(label='Exit')
menu.append(menuitem_translate)
menu.append(menuitem_exit)
menuitem_translate.show()
menuitem_exit.show()
menuitem_exit.connect("activate", gtk.main_quit)
menuitem_translate.connect("activate", lambda self: window.show_all())

tray_icon = TrayIcon(icon, menu, app_id)

buffer1 = gtk.TextBuffer()
buffer2 = gtk.TextBuffer()
buffer3 = gtk.TextBuffer()

textview1.set_buffer(buffer1)
textview2.set_buffer(buffer2)
textview3.set_buffer(buffer3)

# gi.require_version('Keybinder', '3.0')
# from gi.repository import Gdk,Keybinder
# def callback(keystr, user_data):
#     print ("Handling", user_data)
#     print ("Event time:", Keybinder.get_current_event_time())
#     gtk.main_quit()
# keystr = "<Ctrl><Alt>M"
# Keybinder.init()
# Keybinder.bind(keystr, callback)
# print ("Press", keystr, "to handle keybinding and quit")


# def on_accel_pressed(self, *args):
#     print('it works')
#
# from gi.repository import Gdk
# print(Gdk.keyval_from_name('ctrl')) # 16777215
# accel = gtk.AccelGroup()
# accel.connect(Gdk.keyval_from_name('O'), Gdk.ModifierType.CONTROL_MASK, 0, on_accel_pressed)
# window.add_accel_group(accel)


window.show_all()
gtk.main()
