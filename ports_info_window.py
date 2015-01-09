#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gtk_helper
import serial_helper
from main import APP_NAME


class PortInfoWindow:
    def __init__(self, parent_window):
        self.__portsInfoWindow = gtk_helper.GtkGladeHelper.get_glade_window("dlgPortsInfo")
        self.__dlg = gtk_helper.GtkGladeHelper.get_window_control(self.__portsInfoWindow, "dlgPortsInfo")
        self.__tree_view = gtk_helper.GtkGladeHelper.get_window_control(self.__portsInfoWindow, "trPorts")
        self.__dlg.set_transient_for(parent_window)
        self.__dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.__dlg.set_title(APP_NAME)

        self.__add_column("Port name", 0)
        self.__add_column("Description", 1)
        self.__add_column("VID:PID", 2)

        self.port_list = None
        self.__fill_tree_view()

    def __fill_tree_view(self):
        ports = serial_helper.SerialHelper.get_available_ports()
        self.port_list = gtk.ListStore(str, str, str)

        for port in ports:
            self.port_list.append([port[0], port[1], port[2]])

        self.__tree_view.set_model(self.port_list)

    def __add_column(self, title, column_id):
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=column_id)
        column.set_resizable(True)
        column.set_sort_column_id(column_id)
        self.__tree_view.append_column(column)

    def run(self):
        self.__dlg.run()
        self.__dlg.destroy()