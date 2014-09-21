from PySide.QtCore import *
from PySide.QtGui import *

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout=QVBoxLayout()
        self.setLayout(self.layout)


        self.checkbox=QCheckBox("Layouts")
        self.layout.addWidget(self.checkbox)


        self.widget1=QWidget()
        self.layout.addWidget(self.widget1)

        self.layout1=QVBoxLayout()
        self.widget1.setLayout(self.layout1)

        self.layout1.addWidget(QLabel("First layout"))

        self.layout1.addWidget(QTextEdit())


        self.widget2=QWidget()
        self.layout.addWidget(self.widget2)

        self.layout2=QHBoxLayout()
        self.widget2.setLayout(self.layout2)

        self.layout2.addWidget(QTextEdit("Second layout"))

        self.layout2.addWidget(QTextEdit())


        self.checkbox.toggled.connect(self.checkbox_toggled)
        self.checkbox.toggle()

        self.show()

    def checkbox_toggled(self, state):
        self.widget1.setVisible(state)
        self.widget2.setVisible(not state)

app=QApplication([])
mw=MainWindow()
app.exec_()