#!/home/max/DesktopTranslator/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("mainwindow.glade")
window = builder.get_object('window2')
entry = builder.get_object('entry1')
textview1 = builder.get_object('textview4')
textview3 = builder.get_object('textview5')
textview2 = builder.get_object('textview6')

entry.set_text('simple_example')
# input_text = entry.get_text()
# print(input_text)
buffer1 = Gtk.TextBuffer()
buffer2 = Gtk.TextBuffer()
buffer3 = Gtk.TextBuffer()
buffer1.set_text('#1')
buffer2.set_text('#2')
buffer3.set_text('#3')

textview1.set_buffer(buffer1)
textview2.set_buffer(buffer2)
textview3.set_buffer(buffer3)

window.show_all()
Gtk.main()
