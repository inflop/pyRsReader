#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from main import APP_NAME


class GtkGladeHelper:
    @staticmethod
    def show_error_msg(msg, parent_window=None):
        position = Gtk.WindowPosition.CENTER_ALWAYS
        if parent_window is not None:
            position = Gtk.WindowPosition.CENTER_ON_PARENT

        dlg = Gtk.MessageDialog(parent_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, msg)
        dlg.set_position(position)
        dlg.set_title(APP_NAME)
        dlg.run()
        dlg.destroy()

    @staticmethod
    def show_question_msg(question, parent_window=None):
        position = Gtk.WindowPosition.CENTER_ALWAYS
        if parent_window is not None:
            position = Gtk.WindowPosition.CENTER_ON_PARENT

        dlg = Gtk.MessageDialog(parent_window, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, question)
        dlg.set_position(position)
        dlg.set_title(APP_NAME)

        result = dlg.run()
        dlg.destroy()
        return result

    @staticmethod
    def show_info_msg():
        pass
