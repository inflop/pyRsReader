#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import configparser
from main import APP_NAME


class Settings:
    __config_path = "".join([os.path.expanduser("~/."), APP_NAME, ".cfg"])
    __main_section = "Main"
    __port_option_name = "port"
    __baudrate_option_name = "baudrate"
    __autoscroll_option_name = "autoscroll"

    def __init__(self):
        self.__port = ""
        self.__baudrate = ""
        self.__autoscroll = False
        self.__config = configparser.ConfigParser()

        self.__load_settings_from_file()

    @classmethod
    def get_config_file_path(cls):
        return cls.__config_path

    def __load_settings_from_file(self):
        self.__config.read(Settings.__config_path)

        if not self.__config.has_section(Settings.__main_section):
            return

        self.__port = self.__config[Settings.__main_section][Settings.__port_option_name]
        self.__baudrate = self.__config[Settings.__main_section][Settings.__baudrate_option_name]
        self.__autoscroll = eval(self.__config[Settings.__main_section][Settings.__autoscroll_option_name])

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def baudrate(self):
        return self.__baudrate

    @baudrate.setter
    def baudrate(self, value):
        self.__baudrate = value

    @property
    def autoscroll(self):
        return self.__autoscroll

    @autoscroll.setter
    def autoscroll(self, value):
        self.__autoscroll = value

    def save(self):
        if not self.__config.has_section(Settings.__main_section):
            self.__config.add_section(Settings.__main_section)

        self.__config[Settings.__main_section][Settings.__port_option_name] = str(self.__port)
        self.__config[Settings.__main_section][Settings.__baudrate_option_name] = str(self.__baudrate)
        self.__config[Settings.__main_section][Settings.__autoscroll_option_name] = str(self.__autoscroll)

        with open(Settings.__config_path, "w") as configfile:
            self.__config.write(configfile)