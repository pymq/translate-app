import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
window = builder.get_object('window1')
image = builder.get_object('image1')
image.set_from_file('wordcloud.png')
window.show_all()

