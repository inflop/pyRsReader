#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from main import APP_NAME


class GtkGladeHelper:
    def __init__(self, ui_file):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(ui_file)

    @classmethod
    def get_glade_window(cls, name, ui_file):
        builder = Gtk.Builder()
        builder.add_from_file(ui_file)
        return builder.get_object(name)

    @staticmethod
    def get_window_control(window, control_name):
        return window.get_object(control_name)

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
