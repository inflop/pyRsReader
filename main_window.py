#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gi.repository import Gtk, GObject, GLib
import serial
import gtk_helper
import generator_task
import serial_helper
import threading, queue, time
import ports_info_window
import about_window
import settings
from main import APP_NAME
from base_window import BaseWindow

GObject.threads_init()


class MainWindow(BaseWindow):
    def __init__(self):
        BaseWindow.__init__(self, __file__)
        self.__initialize()

    def __initialize(self):
        self.__settings = settings.Settings()

        self.__swScrollWindow = self._builder.get_object("swScrollWindow")
        self.__cbo_ports = self._builder.get_object("cboPorts")
        self.__cbo_baud_rates = self._builder.get_object("cboBaudrates")
        self.__btn_connect = self._builder.get_object("btnConnect")
        self.__btn_connect.set_sensitive(False)
        self.__txt_data = self._builder.get_object("txtData")
        self.__txt_data.set_editable(True)
        #self.__txt_data.connect("size-allocate", self.__autoscroll)
        self.__chkScroll = self._builder.get_object("chkScroll")
        self.__chkScroll.set_active(self.__settings.autoscroll)
        self.__sbStatus = self._builder.get_object("sbStatus")
        self.__fill_baud_rates_combobox()
        self._window.connect("delete-event", self.__on_close, None)
        self.__menu_ports_refresh = self._builder.get_object("mnuPortsRefresh")

        self.__serial = serial.Serial()
        self.__serial_message_queue = queue.Queue()
        self.__reading_thread = None

        self.__refresh_ports()

    def on_mnuPortsDetails_activate(self, widget):
        ports_info_wnd = ports_info_window.PortInfoWindow(self._window)
        ports_info_wnd.run()

    def on_mnuRefresh_activate(self, widget):
        self.__refresh_ports()

    def __refresh_ports(self):
        serial_helper.SerialHelper.refresh()
        self.__fill_ports_combobox()
        self.__refresh_connect_controls_state()

    def on_menuAbout_activate(self, widget):
        about_dlg = about_window.AboutDlg(self._window)
        about_dlg.run()

    def __fill_ports_combobox(self):
        ports_names = serial_helper.SerialHelper.get_available_ports_names()
        default_index = ports_names.index(self.__settings.port) if self.__settings.port in ports_names else 0
        self.__cbo_ports.clear()
        store = Gtk.ListStore(str)
        
        for port in ports_names:
            store.append([port])

        self.__cbo_ports.set_model(store)

        cell = Gtk.CellRendererText()
        self.__cbo_ports.pack_start(cell, True)
        self.__cbo_ports.add_attribute(cell, 'text', 0)

        if len(ports_names) == 1:
            self.__cbo_ports.set_active(0)

        self.__cbo_ports.set_active(default_index)

    def __fill_baud_rates_combobox(self):
        baud_rates = serial_helper.SerialHelper.get_available_baud_rates()
        default_index = baud_rates.index(self.__settings.baudrate)
        store = Gtk.ListStore(str)        

        for baud_rate in baud_rates:
            store.append([baud_rate])

        self.__cbo_baud_rates.set_model(store)
        self.__cbo_baud_rates.set_active(default_index)

    def __refresh_connect_controls_state(self):
        connected = self.__serial.is_open
        self.__btn_connect.set_label("Disconnect" if self.__serial.is_open else "Connect")
        self.__sbStatus.push(0, self.__cbo_ports.get_active_text() + " - Connected" if self.__serial.is_open else "Disconnected")        
        self.__menu_ports_refresh.set_sensitive(not connected)
        self.__cbo_baud_rates.set_sensitive(not connected)
        self.__cbo_ports.set_sensitive(not connected)
        self.__combobox_changed()

    def __combobox_changed(self):
        is_port_selected = self.__cbo_ports.get_active_text() is not None and len(self.__cbo_ports.get_active_text()) > 0
        is_baudrate_selected = self.__cbo_baud_rates.get_active_text() is not None and len(self.__cbo_baud_rates.get_active_text()) > 0
        enable_btn_connect = is_port_selected and is_baudrate_selected
        self.__btn_connect.set_sensitive(enable_btn_connect)

    def on_cboPorts_changed(self, widget):
        self.__combobox_changed()

    def on_cboBaudrates_changed(self, widget):
        self.__combobox_changed()

    def on_btnClear_clicked(self, widget):
        #generator_task.GeneratorTask(lambda: " ", self.__clear).start()
        pass

    def __autoscroll(self, *args):
        autoscroll_checked = self.__chkScroll.get_active()

        if autoscroll_checked:
            adj = self.__swScrollWindow.get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_btnConnect_toggled(self, widget):
        self.__read_data()

    def __read_data(self):
        if not self.__serial.is_open:
            self.__serial.port = self.__cbo_ports.get_active_text()
            self.__serial.baudrate = int(self.__cbo_baud_rates.get_active_text())

            try:
                self.__serial = serial.Serial(self.__serial.port, self.__serial.baudrate)
            except serial.SerialException:
                gtk_helper.GtkGladeHelper.show_error_msg("Selected device can not be found or can not be configured.", self._window)
                self.__btn_connect.set_active(False)
                self.__refresh_ports()
                return

            def gen():
                try:
                    while self.__serial.readable():
                        yield self.__serial.readline().decode("utf-8")
                except serial.SerialException:
                    yield "Selected device can not be found or can not be configured.\n"
                    self.__btn_connect.set_active(False)
                    self.__refresh_ports()

            self.__refresh_text_view_task = generator_task.GeneratorTask(gen, self.__append)
            self.__refresh_text_view_task.start()
        else:
            self.__refresh_text_view_task.stop()
            self.__serial.close()

        self.__refresh_connect_controls_state()

    def reading_serial(self):
        #pass
        # while self.__serial.is_open and self.__serial.readable():
        #     self.__serial_message_queue.put(self.__serial.readline())
        for x in range(100):
            time.sleep(0.2)
            self.__append(str(x)+'\r\n')
            yield True
            # self.__serial_message_queue.put(str(x))
    
    def run_gen(self, function):
        gen = function()
        GLib.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_LOW)

    def __check_serial_message_queue(self):
        if self.__reading_thread.is_alive():
            try:
                serial_message = self.__serial_message_queue.get()
                GLib.idle_add(self.__append, serial_message)
                print(serial_message)
            except queue.Empty:
                pass
            return True # to keep timeout running
        else:
            return False # to end timeout

    def __append(self, *args):
        try:
            self.__txt_data.get_buffer().insert(self.__txt_data.get_buffer().get_end_iter(), *args)
        except:
            pass

    def __clear(self, *args):
        self.__txt_data.get_buffer().set_text("")

    def on_mainWindow_destroy(self, widget):
        self.__quit()

    def __save_settings(self):
        self.__settings.port = self.__cbo_ports.get_active_text()
        self.__settings.baudrate = self.__cbo_baud_rates.get_active_text()
        self.__settings.autoscroll = self.__chkScroll.get_active()
        self.__settings.save()

    def __on_close(self, widget, event, data):
        result = False

        if self.__serial.is_open:
            response = gtk_helper.GtkGladeHelper.show_question_msg(
                "Connection is established. Are you sure you want to quit?", self._window)

            if response == Gtk.ResponseType.YES:
                self.__quit()
                result = False
            else:
                result = True

        if not result:
            self.__save_settings()

        return result

    def __stop_reading_thread(self):
        if not self.__reading_thread is None and self.__reading_thread.is_alive:
            self.__reading_thread.join()

    def __close_port(self):
        if self.__serial.is_open:
            self.__serial.close()
    
    def __quit(self):
        self.__stop_reading_thread()
        self.__close_port()
        Gtk.main_quit()

