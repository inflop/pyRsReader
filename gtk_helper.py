#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from main import APP_NAME

try:
    import pygtk
except:
    pass
try:
    import gtk
    import gtk.glade
    import serial
    import serial.tools.list_ports
except:
    sys.exit(1)


class GtkGladeHelper:
    def __init__(self):
        pass

    __glade_file = "main.glade"

    @classmethod
    def get_glade_window(cls, name):
        return gtk.glade.XML(cls.__glade_file, name)

    @staticmethod
    def get_window_control(window, control_name):
        return window.get_widget(control_name)

    @staticmethod
    def show_error_msg(msg):
        dlg = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, msg)
        dlg.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        dlg.set_title(APP_NAME)
        dlg.run()
        dlg.destroy()

    @staticmethod
    def show_question_msg(question):
        dlg = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, question)
        dlg.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        dlg.set_title(APP_NAME)

        result = dlg.run()
        dlg.destroy()
        return result

    @staticmethod
    def show_info_msg():
        pass
