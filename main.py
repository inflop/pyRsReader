#!/usr/bin/env python

import sys
import threading
import gobject
import thread

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

class SerialHelper:
    def __init__(self):
        self.__available_ports = list(serial.tools.list_ports.comports())

    @property
    def available_ports(self):
        return self.__available_ports

    @property
    def available_ports_names(self):
        return map(lambda port: port[0], self.__available_ports)

    @property
    def available_baud_rates(self):
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


class MainWindow:
    def __init__(self):
        self.__glade_file = "main.glade"
        self.__mainWindow = gtk.glade.XML(self.__glade_file, "mainWindow")
        self.__SerialHelper = SerialHelper()

        self.__cbo_ports = self.__mainWindow.get_widget("cboPorts")
        self.__cbo_baud_rates = self.__mainWindow.get_widget("cboBaudrates")
        self.__btn_connect = self.__mainWindow.get_widget("btnConnect")
        self.__txt_data = self.__mainWindow.get_widget("txtData")
        self.__txt_data.set_editable(True)

        self.__fill_ports_combobox()
        self.__fill_baud_rates_combobox()

        self.__signals = {"on_mainWindow_destroy": self.__destroy,
                          "on_btnConnect_toggled": self.__read_data}
        self.__mainWindow.signal_autoconnect(self.__signals)

        self.__Serial = None
        self.__refresh_text_view_task = None
        self.__is_connected = False

    def __fill_ports_combobox(self):
        store = gtk.ListStore(str)
        ports_names = self.__SerialHelper.available_ports_names

        for port in ports_names:
            store.append([port])

        self.__cbo_ports.set_model(store)

        cell = gtk.CellRendererText()
        self.__cbo_ports.pack_start(cell, True)
        self.__cbo_ports.add_attribute(cell, 'text', 0)

    def __fill_baud_rates_combobox(self):
        store = gtk.ListStore(str)
        baud_rates = self.__SerialHelper.available_baud_rates

        for baud_rate in baud_rates:
            store.append([baud_rate])

        self.__cbo_baud_rates.set_model(store)

        cell = gtk.CellRendererText()
        self.__cbo_baud_rates.pack_start(cell, True)
        self.__cbo_baud_rates.add_attribute(cell, 'text', 0)

    def __refresh_connect_button_state(self):
        if self.__is_connected:
            self.__btn_connect.set_label("Disconnect")
        else:
            self.__btn_connect.set_label("Connect")

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

        self.__refresh_connect_button_state()

    def __append(self, *args):
        self.__txt_data.get_buffer().insert(self.__txt_data.get_buffer().get_end_iter(), *args)

    def __destroy(self, widget):
        if self.__refresh_text_view_task is not None:
            self.__refresh_text_view_task.stop()

        if self.__Serial is not None:
            self.__Serial.close()

        gtk.main_quit()


if __name__ == "__main__":

    if 0 == len(SerialHelper().available_ports):
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "There is no available serial ports")
        md.run()
        md.destroy()
        gtk.main_quit()

    mainWindow = MainWindow()
    gtk.main()

