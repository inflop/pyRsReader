#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports


class SerialHelper:
    def __init__(self):
        pass

    __available_ports = list(serial.tools.list_ports.comports())

    @classmethod
    def get_available_ports(cls):
        return cls.__available_ports

    @classmethod
    def get_available_ports_names(cls):
        return list(map(lambda port: port[0], cls.__available_ports))

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
