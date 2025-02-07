"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['abstract_reader.py']
DATA_FILES = ['arxiv.png', 'play.png' ]
OPTIONS = {'argv_emulation': False, 'includes': ['sip','PySide.QtGui', 'PySide.QtCore', 'sys', 're', 'requests', 'bs4.BeautifulSoup'], 'excludes': ['sympy']}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

