#! /usr/bin/env python
from PySide import QtGui, QtCore
import sys, re
import requests
from bs4 import BeautifulSoup as BS

class ArxivCollector(QtGui.QMainWindow):
    def __init__(self):
        """
        intitialize
        """
        super(ArxivCollector, self).__init__()
        self.links = []
        self.titles = []
        self.abs_contents = []
        self.n_abs = []
        self.CreateMainWindow()
        self.url_list = ['http://arxiv.org/list/astro-ph/new',
                         'http://arxiv.org/list/cond-mat/new',
                         'http://arxiv.org/list/gr-qc/new',
                         'http://arxiv.org/list/hep-ex/new',
                         'http://arxiv.org/list/hep-lat/new',
                         'http://arxiv.org/list/hep-ph/new',
                         'http://arxiv.org/list/hep-th/new',
                         'http://arxiv.org/list/math-ph/new',
                         'http://arxiv.org/list/nlin/new',
                         'http://arxiv.org/list/nucl-ex/new',
                         'http://arxiv.org/list/nucl-th/new',
                         'http://arxiv.org/list/physics/new',
                         'http://arxiv.org/list/quant-ph/new',]


    def CreateMainWindow(self):
        self.Main_Window = QtGui.QWidget()
        # self.list = QtGui.QListView(self.Main_Window)
        # self.model = QtGui.QStandardItemModel(self.list)
        self.category = QtGui.QComboBox(self.Main_Window)
        phy_list = ["Astrophysics",
                    "Condense Matter",
                    "GR and Quantum Cosmology",
                    "High Energy Experiment",
                    "High Energy Lattice",
                    "High Energy Phonomenology",
                    "High Energy Theory",
                    "Mathematical Physics",
                    "Nonlinear Sciences",
                    "Nuclear Experiment",
                    "Nuclear Theory",
                    "Physics",
                    "Quantum Physics"]
        for item in phy_list:
            self.category.addItem(item)
        self.category.setFixedWidth(400)
        self.category.currentIndexChanged.connect(self.refresh)
            
        self.list = QtGui.QListWidget(self.Main_Window)
        self.list.itemDoubleClicked[QtGui.QListWidgetItem].connect(self.test)
        self.list.setMinimumHeight(500)
        self.list.setFixedWidth(400)
        self.refresh_btn = QtGui.QPushButton("Refresh", self.Main_Window)
        self.refresh_btn.setMaximumSize(QtCore.QSize(72, 36))
        self.refresh_btn.pressed.connect(self.refresh)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.category)
        vbox.addWidget(self.list)
        vbox.addWidget(self.refresh_btn)

        self.Main_Window.setLayout(vbox)
        self.setCentralWidget(self.Main_Window)

    def test(self, item):
        print item.text()

    def refresh(self):
        self.CollectAbs()
        self.list.clear()
        for title in self.titles:
            # item = QtGui.QStandardItem(title)
            # self.model.appendRow(item)
            self.list.addItem(QtGui.QListWidgetItem(title))
        # self.list.setModel(self.model) 

    def CollectAbs(self):
        url = self.url_list[self.category.currentIndex()]
        try:
            body = BS(requests.get(url, timeout = 15).text).body
            self.links = map(lambda html:'http://arxiv.org/' + html.contents[2].a.attrs['href'], body.findAll('dt'))
            self.titles = map(lambda html: html.div.div.text.strip(), body.findAll('dd'))
            self.abs_contents = map(lambda html: html.div.p, body.findAll('dd'))
            self.n_abs = len(self.titles)

        except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema) as e:
            pass
            
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = ArxivCollector()
    form.CollectAbs()

    # form.show()
    # sys.exit(app.exec_())
