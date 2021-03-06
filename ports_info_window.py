#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GObject
import gtk_helper
import serial_helper
from base_window import BaseWindow
from main import APP_NAME


class PortInfoWindow(BaseWindow):
    def __init__(self, parent_window):
        BaseWindow.__init__(self, __file__)
        self.__tree_view = self._builder.get_object("trPorts")
        self._window.set_transient_for(parent_window)
        self._window.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

        self.__add_column("Port name", 0)
        self.__add_column("Description", 1)
        self.__add_column("VID:PID", 2)

        self.port_list_store = None
        self.__fill_tree_view()

    def __fill_tree_view(self):
        ports = serial_helper.SerialHelper.get_available_ports()
        self.port_list_store = Gtk.ListStore(str, str, str)

        for port in ports:
            self.port_list_store.append([port[0], port[1], port[2]])

        self.__tree_view.set_model(self.port_list_store)

    def __add_column(self, title, column_id):
        column = Gtk.TreeViewColumn(title, Gtk.CellRendererText(), text=column_id)
        column.set_resizable(True)
        column.set_sort_column_id(column_id)
        self.__tree_view.append_column(column)

    def on_btnClose_clicked(self, widget):
        self.__on_close()

    def __on_close(self):
        self._window.destroy()

    def run(self):
        self._window.run()
        self.__on_close()