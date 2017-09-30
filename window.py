
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, \
    QWidget, QMessageBox, QDesktopWidget, QLineEdit, QPushButton, QGridLayout, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QSize

import sys
from translate import Translator


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Translator'
        self.width = 970 # 840
        self.height = 550 # ?400
        self.tr = Translator()
        self.initUI()

    def initUI(self):
        # self.setWindowIcon(QIcon('icon.png'))
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)
        self.center()

        mainWidget = QWidget()
        grid = QGridLayout()
        grid.setSpacing(8)

        tabstop = 13
        self.inputEdit = QLineEdit()
        self.submitButton = QPushButton('&Translate')
        self.submitButton.setMaximumSize(QSize(100,40))
        self.output1TextEdit = QTextEdit()
        self.output1TextEdit.setTabStopWidth(tabstop)
        self.output2TextEdit = QTextEdit()
        self.output2TextEdit.setTabStopWidth(tabstop)
        self.output3TextEdit = QTextEdit()
        self.output3TextEdit.setTabStopWidth(tabstop)
        self.output4TextEdit = QTextEdit()
        self.output4TextEdit.setTabStopWidth(tabstop)

        grid.addWidget(self.inputEdit, 1, 0)
        grid.addWidget(self.submitButton, 1, 1)
        grid.addWidget(self.output1TextEdit, 2, 0)
        grid.addWidget(self.output2TextEdit, 3, 0)
        grid.addWidget(self.output3TextEdit, 2, 1, 2, 1)
        grid.addWidget(self.output4TextEdit, 2, 2, 2, 1)

        mainWidget.setLayout(grid)
        self.setCentralWidget(mainWidget)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Shift+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        hideAction = QAction('Hide', self)
        hideAction.setShortcut('Ctrl+Q')
        hideAction.setStatusTip('Hide window')
        hideAction.triggered.connect(self.hide)

        showAction = QAction('Show', self)
        # showAction.setShortcut('Ctrl+Q')
        showAction.setStatusTip('Show window')
        showAction.triggered.connect(self.show)

        self.tray = QSystemTrayIcon(QIcon('icon.png'), self)
        traymenu = QMenu()
        traymenu.addAction(showAction)
        traymenu.addAction('Settings')
        traymenu.addAction(exitAction)
        self.tray.setContextMenu(traymenu)
        self.tray.show()

        self.statusBar()

        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(hideAction)

        self.submitButton.pressed.connect(self.translate)

        self.show()

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Enter) or (e.key() == 16777220): # my enter code
            self.translate()

    def translate(self):
        input_text = self.inputEdit.text()
        en_alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                  'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        if input_text.lower()[0] in en_alp or input_text.lower().strip()[1] in en_alp:
            lang = 'en-ru'
        else:
            lang = 'ru-en'

        if lang == 'ru-en':
            self.output1TextEdit.setText('')
        elif lang == 'en-ru':
            self.output1TextEdit.setText(self.tr.translate_google(input_text, lang) + '\n\n\n\nGoogle Translate')

        self.output2TextEdit.setText(self.tr.translate_yandex(input_text, lang) + '\n\n\n\nYandex Translate')
        self.output3TextEdit.setText(self.tr.dictionary_yandex(input_text, lang) + '\n\n\n\nYandex Dictionary')


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sss(self):
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())