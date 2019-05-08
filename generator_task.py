#!/usr/bin/python3
# -*- coding: utf-8 -*-

import _thread
import threading
from gi.repository import GLib


class GeneratorTask(object):
    def __init__(self, generator, loop_callback, complete_callback=None):
        self.generator = generator
        self.loop_callback = loop_callback
        self.complete_callback = complete_callback
        self._stopped = False
        self.thread = None

    def _start(self, *args, **kwargs):
        self._stopped = False
        for ret in self.generator(*args, **kwargs):
            print(ret)
            if self._stopped:
                _thread.exit()
            GLib.idle_add(self._loop, ret)
        if self.complete_callback is not None:
            GLib.idle_add(self.complete_callback)

    def _loop(self, ret):
        if ret is None:
            ret = ()
        if not isinstance(ret, tuple):
            ret = (ret,)
        self.loop_callback(*ret)

    def start(self, *args, **kwargs):
        self.thread = threading.Thread(target=self._start, args=args, kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self._stopped = True
        if self.thread is not None and self.thread.is_alive:
            self.thread.join()
