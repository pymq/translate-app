#!/home/max/DesktopTranslator/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from translate import Translator

builder = gtk.Builder()
builder.add_from_file("mainwindow.glade")


class Handler:
    def onPressedEnter(self, *args):
        if args[1].hardware_keycode == 36:
            input_text = entry.get_text()
            # translate
            tr = Translator()
            buffer1.set_text(tr.translate_google(input_text) + '\n\n\n\nGoogle')
            buffer2.set_text(tr.translate_yandex(input_text) + '\n\n\n\nYandex')

    def onWindowDestroy(self, *args):
        gtk.main_quit()

builder.connect_signals(Handler())
window = builder.get_object('window2')
entry = builder.get_object('entry1')
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
