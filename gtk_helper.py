#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gtk.glade
from main import APP_NAME


class GtkGladeHelper:
    def __init__(self):
        pass

    __glade_file = "data/main.glade"

    @classmethod
    def get_glade_window(cls, name):
        return gtk.glade.XML(cls.__glade_file, name)

    @staticmethod
    def get_window_control(window, control_name):
        return window.get_widget(control_name)

    @staticmethod
    def show_error_msg(msg, parent_window=None):
        position = gtk.WIN_POS_CENTER_ALWAYS
        if parent_window is not None:
            position = gtk.WIN_POS_CENTER_ON_PARENT

        dlg = gtk.MessageDialog(parent_window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, msg)
        dlg.set_position(position)
        dlg.set_title(APP_NAME)
        dlg.run()
        dlg.destroy()

    @staticmethod
    def show_question_msg(question, parent_window=None):
        position = gtk.WIN_POS_CENTER_ALWAYS
        if parent_window is not None:
            position = gtk.WIN_POS_CENTER_ON_PARENT

        dlg = gtk.MessageDialog(parent_window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, question)
        dlg.set_position(position)
        dlg.set_title(APP_NAME)

        result = dlg.run()
        dlg.destroy()
        return result

    @staticmethod
    def show_info_msg():
        pass
