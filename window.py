import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, \
    QWidget, QMessageBox, QDesktopWidget, QLineEdit, QPushButton, QGridLayout, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon, QKeySequence, QKeyEvent
from PyQt5.QtCore import QCoreApplication, Qt, QSize

import sys
from translate import Translator


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Translator'
        self.width = 920
        self.height = 620
        self.tr = Translator()
        self.curr_pos = 0
        self.history = []
        self.history_uploaded = 0
        self.read_history(10)
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
        self.submitButton.setMaximumSize(QSize(100, 40))
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

        translateAction = QAction('Translate', self.inputEdit)
        translateAction.setShortcuts([16777220, Qt.CTRL + Qt.Key_Space, Qt.Key_Enter])
        translateAction.setStatusTip('Translate')
        translateAction.triggered.connect(self.translate)

        # downAction = QAction('History backward', self.inputEdit)
        # downAction.setShortcuts([Qt.Key_Down, 16777237])
        # downAction.setStatusTip('History backward')
        # downAction.triggered.connect(self.navigate_history_backward)
        #
        # upAction = QAction('History forward', self)
        # upAction.setShortcuts([Qt.Key_Up, 16777235])
        # upAction.setStatusTip('History forward')
        # upAction.triggered.connect(self.navigate_history_forward)

        showAction = QAction('Show', self)
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
        fileMenu.addAction(translateAction)

        self.submitButton.pressed.connect(self.translate)

        # self.inputEdit.installEventFilter(self)

        self.show()

    # def eventFilter(self, QObject, QEvent):
    #     if QObject == self.inputEdit:
    #         if QEvent == QEvent.KeyPress:
    #             if QEvent.key() == Qt.Key_Down or QEvent.key() == Qt.Key_Up:
    #                 self.output4TextEdit.setText("it works!")
    #     return super().eventFilter(QObject, QEvent)

    def navigate_history_backward(self):
        # key down is 16777237
        if self.curr_pos <= 0:
            return
        self.curr_pos -= 1
        self.inputEdit.setText(self.history[self.curr_pos])
        self.inputEdit.selectAll()
        pass

    def navigate_history_forward(self):
        # key up is 16777235
        if self.curr_pos >= (len(self.history) - 1):
            return
        self.curr_pos += 1
        self.inputEdit.setText(self.history[self.curr_pos])
        self.inputEdit.selectAll()
        pass

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Up:
            self.navigate_history_forward()
        if QKeyEvent.key() == Qt.Key_Down:
            self.navigate_history_backward()

    def read_history(self, n):
        fname = "history.txt"
        if not os.path.exists(fname):
            return
        with open(fname, "r") as f:
            f.seek(0, 2)
            fsize = f.tell()
            f.seek(max(fsize - 2048, 0), 0)
            lines = f.readlines()

        lines_list = [line.rstrip() for line in lines[-n:]]
        self.history.extend(lines_list)
        self.history_uploaded = len(lines_list)
        # делаем на 1 больше максимума, чтобы при нажатии вниз попадать на последнюю запись
        self.curr_pos = len(self.history)

    def write_history(self):
        fname = "history.txt"
        isnew = True
        if os.path.exists(fname):
            isnew = False
        with open(fname,'a') as f:
            if not isnew:
                f.write('\n')
            f.write('\n'.join(self.history[self.history_uploaded -1:]))

    def translate(self):
        input_text = self.inputEdit.text()
        if input_text.isspace():
            return
        en_alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                  'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        if input_text.lower()[0] in en_alp or input_text.lower().strip()[1] in en_alp:
            lang = 'en-ru'
            self.output1TextEdit.setText(self.tr.translate_google(input_text, lang) + '\n'*4 + 'Google Translate')
        else:
            lang = 'ru-en'
            self.output1TextEdit.setText('')

        self.output2TextEdit.setText(self.tr.translate_yandex(input_text, lang) + '\n'*4 + 'Yandex Translate')
        self.output3TextEdit.setText(self.tr.dictionary_yandex(input_text, lang) + '\n'*4 + 'Yandex Dictionary')

        self.inputEdit.selectAll()
        self.history.append(input_text)
        self.curr_pos = len(self.history) - 1

    def closeEvent(self, QCloseEvent):
        if len(self.history) == 0 or len(self.history) == self.history_uploaded:
            super().closeEvent(QCloseEvent)
            return

        self.write_history()
        super().closeEvent(QCloseEvent)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())