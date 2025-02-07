#! /usr/bin/env python
from PySide import QtGui, QtCore
import sys, re
import requests
import webbrowser
from bs4 import BeautifulSoup as BS
from arxiv_collector import ArxivCollector


class AbstractReader(QtGui.QMainWindow):
    def __init__(self):
        """
        initialization
        aim: to build a application that helps me to read the abstract of paper
        """
        super(AbstractReader, self).__init__()
        self.setWindowTitle("Abstract Reader")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Play_Next)
        self.word_list = []
        self.sentence_list = []
        self.isPlay = False
        self.current_word_i = 0
        self.n_word = 0
        self.ind = 0
        self.CreateMainWindow()
        self.CreateStatusBar()

    def CreateMainWindow(self):
        """
        create the main widget of this program
        """
        self.Main_Window = QtGui.QWidget()
        self.Display_Line = QtGui.QLabel("", self.Main_Window)
        self.Display_Line.setAlignment(QtCore.Qt.AlignHCenter)
        self.Display_Line.setFont(QtGui.QFont('Helvetica', pointSize=48))
        self.Display_Line.setText("<b>A</b><SUP>bs</SUP><SUB>tract</SUB> <b>R</b>eader")

        self.Title_Line = QtGui.QLabel("", self.Main_Window)
        self.Title_Line.setFont(QtGui.QFont('Helvetica', pointSize = 18, italic = True))
        self.Title_Line.setWordWrap(True)
        
        self.showlist_btn = QtGui.QCheckBox("Play List")
        self.showlist_btn.toggled.connect(self.ShowList)

        self.play_btn = QtGui.QPushButton("", self.Main_Window)
        self.play_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
        self.play_btn.setMaximumSize(QtCore.QSize(48, 36))
        self.play_btn.pressed.connect(self.Play_Text)

        self.stop_btn = QtGui.QPushButton("", self.Main_Window)
        self.stop_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaStop))
        self.stop_btn.setMaximumSize(QtCore.QSize(48, 36))
        self.stop_btn.pressed.connect(self.Stop)

        self.next_btn = QtGui.QPushButton("", self.Main_Window)
        self.next_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaSkipForward))
        self.next_btn.setMaximumSize(QtCore.QSize(48, 36))
        self.next_btn.pressed.connect(self.Next)
        
        self.previous_btn = QtGui.QPushButton("", self.Main_Window)
        self.previous_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaSkipBackward))
        self.previous_btn.setMaximumSize(QtCore.QSize(48, 36))
        self.previous_btn.pressed.connect(self.Previous)

        self.speed_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.speed_slider.setRange(200, 500)
        self.speed_slider.setValue(280)
        self.speed = 280.0
        self.speed_slider.setTracking(True)
        self.speed_slider.setTickPosition(QtGui.QSlider.TicksBothSides)

        self.abstract_text = QtGui.QTextEdit("", self.Main_Window)
        self.abstract_text.textChanged.connect(self.Start_Over)
        self.abstract_text.setFixedHeight(280)

        PlayControlPanel = QtGui.QHBoxLayout()
        PlayControlPanel.addWidget(self.previous_btn)
        PlayControlPanel.addWidget(self.play_btn)
        PlayControlPanel.addWidget(self.stop_btn)
        PlayControlPanel.addWidget(self.next_btn)
        PlayControlPanel.addSpacing(18)
        PlayControlPanel.addWidget(QtGui.QLabel("Speed:"))
        PlayControlPanel.addWidget(self.speed_slider)

        self.url_line = QtGui.QLineEdit("", self.Main_Window)
        self.url_line.returnPressed.connect(self.Arxiv_Parser)
        self.url_line.setFocus()

        self.arxiv_btn = QtGui.QPushButton("ARXIV", self.Main_Window)
        #self.arxiv_btn.setIcon(QtGui.QIcon("arxiv.png"))
        #self.arxiv_btn.setMaximumSize(QtCore.QSize(80,40))
        #self.arxiv_btn.setFlat(True)
        #self.arxiv_btn.setIconSize(QtCore.QSize(18,18))
        self.arxiv_btn.pressed.connect(self.Arxiv_Parser)
        self.open_btn = QtGui.QPushButton("Open", self.Main_Window)
        self.open_btn.pressed.connect(self.Open_in_Browser)

        ArxivLine = QtGui.QHBoxLayout()
        ArxivLine.addWidget(self.url_line)
        ArxivLine.addSpacing(12)
        ArxivLine.addWidget(self.open_btn)
        ArxivLine.addWidget(self.arxiv_btn)

        DisplayBox = QtGui.QVBoxLayout()
        DisplayBox.addSpacing(24)
        DisplayBox.addWidget(self.Display_Line)
        DisplayBox.addSpacing(36)
        DisplayBox.addWidget(self.Title_Line)
        DisplayBox.addWidget(self.abstract_text)
        DisplayBox.addLayout(ArxivLine)
        DisplayBox.addLayout(PlayControlPanel)
        DisplayBox.addWidget(self.showlist_btn)

        self.playlist = ArxivCollector()
        #self.playlist.list.itemClicked[QtGui.QListWidgetItem].connect(self.ShowTitle)
        self.playlist.list.itemClicked[QtGui.QListWidgetItem].connect(self.PaperSelected)
        OutBox = QtGui.QHBoxLayout()
        self.widget2 = QtGui.QWidget()
        self.layout2 = QtGui.QHBoxLayout()
        self.layout2.addWidget(self.playlist)
        self.widget2.setLayout(self.layout2)
        OutBox.addWidget(self.widget2)
        OutBox.addLayout(DisplayBox)
        self.showlist_btn.toggle()
        self.Main_Window.setLayout(OutBox)
        self.setCentralWidget(self.Main_Window)

    def ShowList(self, state):
        """
        play list control function
        to highlight current item
        """
        self.widget2.setVisible(state)

    def CreateStatusBar(self):
        """create status bar"""
        self.status_text = QtGui.QLabel("Welcome to arXiv")
        self.statusBar().addWidget(self.status_text, 1)

    def PrePare_Text(self):
        """prepare for displaying"""
        if self.abstract_text.toPlainText() == '':
            pass

        else:
            self.word_list = map(lambda x: x.strip(), self.abstract_text.toPlainText().strip().split())
            self.n_word = len(self.word_list)
            self.current_word_i = 0
            self.sentence_list = map(lambda x: x.strip(), self.abstract_text.toPlainText().strip().split('.'))

    def Play_Text(self):
        self.isPlay = ~self.isPlay
        if self.isPlay:
            self.play_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPause))
        else:
            self.play_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))

        if len(self.word_list) == 0:
            self.PrePare_Text()

        if len(self.word_list) == 0:
            self.isPlay = False
            self.play_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
            self.statusBar().showMessage("Stoped!")
            return None
        else:
            self.Display_Line.setText(self.word_list[self.current_word_i])
        while self.current_word_i < self.n_word and self.isPlay:
            self.statusBar().showMessage("Playing at speed of {0} words/min".format(int(self.speed)))
            QtGui.QApplication.processEvents()
            if (not self.timer.isActive()) and self.isPlay:
                try:
                    self.timer.start(self.Interval_Time(self.word_list[self.current_word_i]) * 1000)
                except IndexError:
                    break

        self.statusBar().showMessage("Stoped!")

    def Play_Next(self):
        self.current_word_i += 1
        if self.current_word_i == self.n_word:
            self.isPlay = False
            self.play_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
            self.current_word_i = 0
        else:
            self.Display_Line.setText(self.word_list[self.current_word_i])
        self.timer.stop()

    def Next(self):
        if self.ind <  self.playlist.n_abs - 1:
            self.ind += 1
        self.MakeText()

    def Previous(self):
        if self.ind > 0:
            self.ind -= 1
        self.MakeText()


    def Interval_Time(self, word):
        self.speed = float(self.speed_slider.value())
        base_time = 60.0 / self.speed
        if len(word) <= 3:
            base_time = base_time * 0.9
        elif len(word) >= 8:
            base_time = base_time * 1.2
        if word[-1] == '.':
            base_time = base_time + 0.2

        return base_time

    def Arxiv_Parser(self):
        """Parse an arxiv url"""
        url = self.url_line.text()
        if not re.search(r'arxiv.org/*abs', url):
            self.statusBar().showMessage("Wrong URL!")
            return None
        try:
            arxiv = requests.get(url, timeout=10, stream = True)
            ab_content = BS(arxiv.text)
            self.abstract_text.setText(ab_content.blockquote.text.replace('\n', ' ').strip('Abstract: '))
            self.statusBar().showMessage("Abstract obtained from: {0}".format(url))
            self.PrePare_Text()
        except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema) as e:
            self.statusBar().showMessage("Request timeout! Wrong URL?")
            self.abstract_text.setText("")

    def Open_in_Browser(self):
        url = self.url_line.text()
        webbrowser.open(url)

    def Stop(self):
        self.timer.stop()
        self.isPlay = False
        self.play_btn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
        self.current_word_i = 0
        self.Display_Line.setText("<b>A</b><SUP>bs</SUP><SUB>tract</SUB> <b>R</b>eader")

    def Start_Over(self):
        self.Stop()
        self.word_list = []
        self.sentence_list = []

    def PaperSelected(self, item):
        self.ind = self.playlist.titles.index(item.text())
        self.MakeText()

    def MakeText(self):
        self.Stop()
        self.playlist.list.setCurrentItem(self.playlist.list.item(self.ind))
        self.url_line.setText(self.playlist.links[self.ind])
        self.statusBar().showMessage(self.playlist.titles[self.ind])
        self.Title_Line.setText(self.playlist.titles[self.ind])
        try:
            self.abstract_text.setText(self.playlist.abs_contents[self.ind].text.replace("\n", " "))
        except AttributeError:
            #self.abstract_text.setText("")
            self.Arxiv_Parser()

    def ShowTitle(self, item):
        self.statusBar().showMessage(item.text())

        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = AbstractReader()
    form.resize(1000, 500)
    form.show()
    sys.exit(app.exec_())

        
