#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import gtk_helper
from base_window import BaseWindow
from main import APP_NAME


class AboutDlg(BaseWindow):
    def __init__(self, parent_window):
        BaseWindow.__init__(self, __file__)
        self._window.set_transient_for(parent_window)
        self._window.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
    
    def __on_close(self):
        self._window.destroy()

    def run(self):
        self._window.run()
        self.__on_close()

    def on_btnClose_clicked(self, widget):
        self.__on_close()
