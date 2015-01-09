from distutils.core import setup
import glob
import os
import sys
import platform

if platform.system() == 'Windows':
    import py2exe

__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]

if platform.system() == 'Windows':
    setup(
        name='pyRsReader',
        version='0.0.1',
        url='https://github.com/inflop/pyRsReader',
        license='GPL',
        author='infloper',
        author_email='infloper@gmail.com',
        description='Simple RS232 reader written in Python using pySerial and PyGTK library',
        data_files=[("", glob.glob("main.glade")), os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'), os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll')],
        options={'py2exe': {'packages': 'encodings', 'includes': 'ctypes, cairo, pango, pangocairo, atk, gio'}},
        scripts=[
            "main.py",
            "gtk_helper.py",
            "serial_helper.py",
            "generator_task.py",
            "main_window.py",
            "ports_info_window.py",
            "about_window.py"
            ],
        windows=[{"script": "main.py"}],
        requires=['pygtk']
    )
else:
    setup(
        name='pyRsReader',
        version='0.0.1',
        url='https://github.com/inflop/pyRsReader',
        license='GPL',
        author='infloper',
        author_email='infloper@gmail.com',
        description='Simple RS232 reader written in Python using pySerial and PyGTK library',
        data_files=[("", glob.glob("main.glade"))],
        scripts=[
            "main.py",
            "gtk_helper.py",
            "serial_helper.py",
            "generator_task.py",
            "main_window.py",
            "ports_info_window.py",
            "about_window.py"
            ],
        requires=['pygtk']
    )