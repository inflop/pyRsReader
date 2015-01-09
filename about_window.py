#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gtk_helper
from main import APP_NAME


class AboutDlg:
    def __init__(self, parent_window):
        self.__dlgAbout = gtk_helper.GtkGladeHelper.get_glade_window("dlgAbout")
        self.__dlg = gtk_helper.GtkGladeHelper.get_window_control(self.__dlgAbout, "dlgAbout")
        self.__dlg.set_transient_for(parent_window)
        self.__dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.__dlg.set_title(APP_NAME)

    def run(self):
        self.__dlg.run()
        self.__dlg.destroy()