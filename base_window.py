#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from gi.repository import Gtk
from main import APP_NAME


class BaseWindow:
    def __init__(self, filename=__file__):
        self.__ui_filename = os.path.splitext(
            os.path.basename(filename))[0] + ".ui"

        self.__initialize()

    def __initialize(self):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(self.__ui_filename)
        self._builder.connect_signals(self)
        self._window = self._builder.get_object("window")
        self._window.set_title(APP_NAME)
        self._window.show_all()

