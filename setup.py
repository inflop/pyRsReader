from distutils.core import setup
import py2exe
import glob
import os
import sys

__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]

setup(
    name='pyRsReader',
    version='0.0.1',
    url='https://github.com/inflop/pyRsReader',
    license='GPL',
    author='Rafal Klepacz',
    author_email='infloper@gmail.com',
    description='Simple RS232 reader written in Python using pySerial and PyGTK library',
    data_files=[("", glob.glob("main.glade")), os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'), os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll')],
    options={'py2exe': {'packages': 'encodings', 'includes': 'ctypes, cairo, pango, pangocairo, atk, gobject, gio, gtk, gtk.glade, glib'}},
    scripts=["main.py"],
    windows=[{"script": "main.py"}]
)
