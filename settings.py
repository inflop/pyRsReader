#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ConfigParser
from main import APP_NAME


class Settings:
    __config_path = "".join([os.path.expanduser("~\\"), ".", APP_NAME, ".cfg"])
    __main_section = "Main"
    __port_option_name = "port"
    __baudrate_option_name = "baudrate"
    __autoscroll_option_name = "autoscroll"

    def __init__(self):
        self.__port = ""
        self.__baudrate = ""
        self.__autoscroll = False
        self.__config = ConfigParser.ConfigParser()

        self.__load_settings_from_file()

    def __load_settings_from_file(self):
        self.__config.read(Settings.__config_path)

        if not self.__config.has_section(Settings.__main_section):
            return

        self.__port = self.__config.get(Settings.__main_section, Settings.__port_option_name)
        self.__baudrate = self.__config.get(Settings.__main_section, Settings.__baudrate_option_name)
        self.__autoscroll = self.__config.getboolean(Settings.__main_section, Settings.__autoscroll_option_name)

    def set_port(self, value):
        self.__port = value

    def get_port(self):
        return self.__port

    def set_baudrate(self, value):
        self.__baudrate = value

    def get_baudrate(self):
        return self.__baudrate

    def set_autoscroll(self, value):
        self.__autoscroll = value

    def get_autoscroll(self):
        return self.__autoscroll

    def save(self):
        if not self.__config.has_section(Settings.__main_section):
            self.__config.add_section(Settings.__main_section)

        self.__config.set(Settings.__main_section, Settings.__port_option_name, self.__port)
        self.__config.set(Settings.__main_section, Settings.__baudrate_option_name, self.__baudrate)
        self.__config.set(Settings.__main_section, Settings.__autoscroll_option_name, self.__autoscroll)

        with open(Settings.__config_path, "wb") as configfile:
            self.__config.write(configfile)