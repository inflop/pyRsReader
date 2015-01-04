#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Rafał Klepacz"
__copyright__ = "Copyright 2015, The Inflop Project"
__credits__ = ["Rafał Klepacz"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Rafał Klepacz"
__email__ = "infloper@gmail.com"
__status__ = "BETA"

import sys
import threading
import gobject
import thread
import logging

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
    import serial
    import serial.tools.list_ports
except:
    sys.exit(1)

gtk.gdk.threads_init()

APP_NAME = "pyRsReader"


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
        dlg.set_title(APP_NAME)
        dlg.run()
        dlg.destroy()
        gtk.main_quit()


class SerialHelper:
    def __init__(self):
        pass

    __available_ports = list(serial.tools.list_ports.comports())

    @classmethod
    def get_available_ports(cls):
        return cls.__available_ports

    @classmethod
    def get_available_ports_names(cls):
        return map(lambda port: port[0], cls.__available_ports)

    @staticmethod
    def get_available_baud_rates():
        return ["300",
                "1200",
                "2400",
                "4800",
                "9600",
                "14400",
                "19200",
                "28800",
                "38400",
                "57600",
                "115200"]

    @classmethod
    def refresh(cls):
        cls.__available_ports = list(serial.tools.list_ports.comports())


class GeneratorTask(object):
    def __init__(self, generator, loop_callback, complete_callback=None):
        self.generator = generator
        self.loop_callback = loop_callback
        self.complete_callback = complete_callback
        self._stopped = False

    def _start(self, *args, **kwargs):
        self._stopped = False
        for ret in self.generator(*args, **kwargs):
            if self._stopped:
                thread.exit()
            gobject.idle_add(self._loop, ret)
        if self.complete_callback is not None:
            gobject.idle_add(self.complete_callback)

    def _loop(self, ret):
        if ret is None:
            ret = ()
        if not isinstance(ret, tuple):
            ret = (ret,)
        self.loop_callback(*ret)

    def start(self, *args, **kwargs):
        threading.Thread(target=self._start, args=args, kwargs=kwargs).start()

    def stop(self):
        self._stopped = True


class PortInfoWindow:
    def __init__(self, parent_window):
        self.__portsInfoWindow = GtkGladeHelper.get_glade_window("dlgPortsInfo")
        self.__dlg = GtkGladeHelper.get_window_control(self.__portsInfoWindow, "dlgPortsInfo")
        self.__tree_view = GtkGladeHelper.get_window_control(self.__portsInfoWindow, "trPorts")
        self.__dlg.set_transient_for(parent_window)
        self.__dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.__dlg.set_title(APP_NAME)

        self.__add_column("Port name", 0)
        self.__add_column("Description", 1)
        self.__add_column("VID:PID", 2)

        self.port_list = None
        self.__fill_tree_view()

    def __fill_tree_view(self):
        ports = SerialHelper.get_available_ports()
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


class AboutDlg:
    def __init__(self, parent_window):
        self.__dlgAbout = GtkGladeHelper.get_glade_window("dlgAbout")
        self.__dlg = GtkGladeHelper.get_window_control(self.__dlgAbout, "dlgAbout")
        self.__dlg.set_transient_for(parent_window)
        self.__dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.__dlg.set_title(APP_NAME)

    def run(self):
        self.__dlg.run()
        self.__dlg.destroy()


class MainWindow:
    def __init__(self):
        self.__mainWindow = GtkGladeHelper.get_glade_window("mainWindow")
        self.__mainWindowWidget = GtkGladeHelper.get_window_control(self.__mainWindow, "mainWindow")
        self.__mainWindowWidget.set_title(APP_NAME)

        self.__cbo_ports = GtkGladeHelper.get_window_control(self.__mainWindow, "cboPorts")
        self.__cbo_baud_rates = GtkGladeHelper.get_window_control(self.__mainWindow, "cboBaudrates")
        self.__btn_connect = GtkGladeHelper.get_window_control(self.__mainWindow, "btnConnect")
        self.__txt_data = GtkGladeHelper.get_window_control(self.__mainWindow, "txtData")
        self.__txt_data.set_editable(True)

        self.__fill_ports_combobox()
        self.__fill_baud_rates_combobox()

        self.__signals = {"on_mainWindow_destroy": self.__destroy,
                          "on_btnConnect_toggled": self.__read_data,
                          "on_mnuPortsDetails_activate": self.__port_info_activate,
                          "on_mnuRefresh_activate": self.__refresh_ports,
                          "on_menuAbout_activate": self.__about_dlg_activate}
        self.__mainWindow.signal_autoconnect(self.__signals)

        self.__Serial = None
        self.__refresh_text_view_task = None
        self.__is_connected = False

    def __port_info_activate(self, widget):
        ports_info_wnd = PortInfoWindow(self.__mainWindowWidget)
        ports_info_wnd.run()

    def __refresh_ports(self, widget):
        SerialHelper.refresh()
        self.__fill_ports_combobox()

    def __about_dlg_activate(self, widget):
        about_dlg = AboutDlg(self.__mainWindowWidget)
        about_dlg.run()

    def __fill_ports_combobox(self):
        self.__cbo_ports.set_model(None)
        self.__cbo_ports.clear()
        store = gtk.ListStore(str)
        ports_names = SerialHelper.get_available_ports_names()

        for port in ports_names:
            store.append([port])

        self.__cbo_ports.set_model(store)

        cell = gtk.CellRendererText()
        self.__cbo_ports.pack_start(cell, True)
        self.__cbo_ports.add_attribute(cell, 'text', 0)

    def __fill_baud_rates_combobox(self):
        store = gtk.ListStore(str)
        baud_rates = SerialHelper.get_available_baud_rates()

        for baud_rate in baud_rates:
            store.append([baud_rate])

        self.__cbo_baud_rates.set_model(store)

        cell = gtk.CellRendererText()
        self.__cbo_baud_rates.pack_start(cell, True)
        self.__cbo_baud_rates.add_attribute(cell, 'text', 0)

    def __refresh_connect_controls_state(self):
        if self.__is_connected:
            self.__btn_connect.set_label("Disconnect")
        else:
            self.__btn_connect.set_label("Connect")

        GtkGladeHelper.get_window_control(self.__mainWindow, "mnuPortsRefresh").set_sensitive(not self.__is_connected)
        self.__cbo_baud_rates.set_sensitive(not self.__is_connected)
        self.__cbo_ports.set_sensitive(not self.__is_connected)

    def __read_data(self, widget):
        if not self.__is_connected:
            selected_port = self.__cbo_ports.get_active_text()
            baud_rate = int(self.__cbo_baud_rates.get_active_text())
            self.__Serial = serial.Serial(selected_port, baud_rate)
            self.__is_connected = True

            def gen():
                while self.__Serial.readable():
                    yield self.__Serial.readline()

            self.__refresh_text_view_task = GeneratorTask(gen, self.__append)
            self.__refresh_text_view_task.start()
        else:
            self.__refresh_text_view_task.stop()
            self.__Serial.close()
            self.__is_connected = False

        self.__refresh_connect_controls_state()

    def __append(self, *args):
        self.__txt_data.get_buffer().insert(self.__txt_data.get_buffer().get_end_iter(), *args)

    def __destroy(self, widget):
        if self.__refresh_text_view_task is not None:
            self.__refresh_text_view_task.stop()

        if self.__Serial is not None:
            self.__Serial.close()

        gtk.main_quit()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    if len(SerialHelper.get_available_ports()) == 0:
        GtkGladeHelper.show_error_msg("There is no available serial ports")
        gtk.main_quit()

    mainWindow = MainWindow()
    gtk.main()

