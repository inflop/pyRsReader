#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "infloper"
__copyright__ = "Copyright 2015, The Inflop Project"
__credits__ = ["infloper"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "infloper"
__email__ = "infloper@gmail.com"
__status__ = "BETA"

APP_NAME = "pyRsReader"

import sys
import gtk
import gtk_helper
import serial_helper
import main_window

gtk.gdk.threads_init()

if __name__ == "__main__":
    if len(serial_helper.SerialHelper.get_available_ports()) == 0:
        gtk_helper.GtkGladeHelper.show_error_msg("There are no available serial ports")
        sys.exit()

    mainWindow = main_window.MainWindow()
    gtk.main()

