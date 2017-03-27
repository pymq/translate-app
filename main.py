#!/home/max/DesktopTranslator/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from translate import Translator

builder = gtk.Builder()
builder.add_from_file("mainwindow.glade")


class Handler:
    def __init__(self):
        self.on_entry_grab_focus()
        return

    def on_entry_key_press_event(self, *args):
        if args[1].hardware_keycode == 36:
            input_text = entry.get_text()
            # translate
            tr = Translator()
            buffer1.set_text(tr.translate_google(input_text) + '\n\n\n\nGoogle Translate')
            buffer2.set_text(tr.translate_yandex(input_text) + '\n\n\n\nYandex Translate')
            buffer3.set_text(tr.dictionary_yandex(input_text) + '\n\n\n\nYandex Dictionary')

    def onWindowDestroy(self, *args):
        gtk.main_quit()

    #TODO: focus
    def on_entry_grab_focus(self, *args):
        return

    #TODO: switcher

builder.connect_signals(Handler())
window = builder.get_object('window')
entry = builder.get_object('entry')
textview1 = builder.get_object('textview4')
textview2 = builder.get_object('textview5')
textview3 = builder.get_object('textview6')

buffer1 = gtk.TextBuffer()
buffer2 = gtk.TextBuffer()
buffer3 = gtk.TextBuffer()

textview1.set_buffer(buffer1)
textview2.set_buffer(buffer2)
textview3.set_buffer(buffer3)

window.show_all()
gtk.main()
