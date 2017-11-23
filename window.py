import os
import sys

import requests
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, \
    QWidget, QMessageBox, QDesktopWidget, QLineEdit, QPushButton, QGridLayout, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon, QKeySequence, QKeyEvent
from PyQt5.QtCore import QCoreApplication, Qt, QSize

from translate import Translator
from history import History


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Translator'
        self.width = 920
        self.height = 620
        self.tr = Translator()
        self.history = History("history.txt", 10)
        self.threads = [None for _ in range(5)]
        self.init_UI()

    def init_UI(self):
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
        self.text_edit_1 = QTextEdit()
        self.text_edit_1.setTabStopWidth(tabstop)
        self.text_edit_2 = QTextEdit()
        self.text_edit_2.setTabStopWidth(tabstop)
        self.text_edit_3 = QTextEdit()
        self.text_edit_3.setTabStopWidth(tabstop)
        self.text_edit_4 = QTextEdit()
        self.text_edit_4.setTabStopWidth(tabstop)
        self.text_edit_5 = QTextEdit()
        self.text_edit_5.setTabStopWidth(tabstop)

        grid.addWidget(self.inputEdit, 1, 0)
        grid.addWidget(self.submitButton, 1, 1)
        grid.addWidget(self.text_edit_1, 2, 0)
        grid.addWidget(self.text_edit_2, 3, 0)
        grid.addWidget(self.text_edit_3, 2, 1, 2, 1)
        grid.addWidget(self.text_edit_4, 2, 2)
        grid.addWidget(self.text_edit_5, 3, 2)

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
        self.history.navigate_back()
        self.inputEdit.setText(self.history.current_word)
        self.inputEdit.selectAll()

    def navigate_history_forward(self):
        # key up is 16777235
        self.history.navigate_forward()
        self.inputEdit.setText(self.history.current_word)
        self.inputEdit.selectAll()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Up:
            self.navigate_history_forward()
        if QKeyEvent.key() == Qt.Key_Down:
            self.navigate_history_backward()


    def translate(self):
        input_text = self.inputEdit.text().strip().lower()
        if input_text == '':
            self.inputEdit.setText('')
            return
        en_alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                  'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        if input_text.lower()[0] in en_alp or input_text[1] in en_alp:
            lang = 'en-ru'
        else:
            lang = 'ru-en'

        for i in range(5):
            if self.threads[i]:
                self.threads[i].terminate()
                self.threads[i] = None
        self.workers = [None for _ in range(5)]

        if lang is 'en-ru':
            self.threads[0] = QThread()
            self.workers[0] = Worker(input_text, lang, self.tr)
            self.workers[0].result[str].connect(self.TE_1_set_text)
            self.workers[0].moveToThread(self.threads[0])
            self.threads[0].started.connect(self.workers[0].translate_google)
            self.threads[0].finished.connect(self.threads[0].exit)
            self.threads[0].finished.connect(self.threads[0].quit)
            self.threads[0].start()

            self.threads[3] = QThread()
            self.workers[3] = Worker(input_text, 'en-en', self.tr)
            self.workers[3].result[str].connect(self.TE_4_set_text)
            self.workers[3].moveToThread(self.threads[3])
            self.threads[3].started.connect(self.workers[3].synonym)
            self.threads[3].finished.connect(self.threads[3].exit)
            self.threads[3].finished.connect(self.threads[3].quit)
            self.threads[3].start()

            self.threads[4] = QThread()
            self.workers[4] = Worker(input_text, 'en-en', self.tr)
            self.workers[4].result[str].connect(self.TE_5_set_text)
            self.workers[4].moveToThread(self.threads[4])
            self.threads[4].started.connect(self.workers[4].definition)
            self.threads[4].finished.connect(self.threads[4].exit)
            self.threads[4].finished.connect(self.threads[4].quit)
            self.threads[4].start()

        elif lang is 'ru-en':
            self.text_edit_1.setText('')
            self.text_edit_4.setText('')
            self.text_edit_5.setText('')

        self.threads[1] = QThread()
        self.workers[1] = Worker(input_text, lang, self.tr)
        self.workers[1].result[str].connect(self.TE_2_set_text)
        self.workers[1].moveToThread(self.threads[1])
        self.threads[1].started.connect(self.workers[1].translate_yandex)
        self.threads[1].finished.connect(self.threads[1].exit)
        self.threads[1].finished.connect(self.threads[1].quit)
        self.threads[1].start()

        self.threads[2] = QThread()
        self.workers[2] = Worker(input_text, lang, self.tr)
        self.workers[2].result[str].connect(self.TE_3_set_text)
        self.workers[2].moveToThread(self.threads[2])
        self.threads[2].started.connect(self.workers[2].dictionary_yandex)
        self.threads[2].finished.connect(self.threads[2].exit)
        self.threads[2].finished.connect(self.threads[2].quit)
        self.threads[2].start()

        self.inputEdit.selectAll()
        self.history.append(input_text)

    @pyqtSlot(str)
    def TE_1_set_text(self, s):
        self.text_edit_1.setText('Google Translate\n\n' + s)

    @pyqtSlot(str)
    def TE_2_set_text(self, s):
        self.text_edit_2.setText('Yandex Translate\n\n' + s)

    @pyqtSlot(str)
    def TE_3_set_text(self, s):
        self.text_edit_3.setText('Yandex Dictionary\n\n' + s)

    @pyqtSlot(str)
    def TE_4_set_text(self, s):
        self.text_edit_4.setText(s)

    @pyqtSlot(str)
    def TE_5_set_text(self, s):
        self.text_edit_5.setText(s)

    def closeEvent(self, QCloseEvent):
        self.history.upload_history()
        super().closeEvent(QCloseEvent)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Worker(QObject):
    result = pyqtSignal(str)

    def __init__(self, input_text, lang, translator):
        self.tr = translator
        self.lang = lang
        self.input_text = input_text
        super().__init__()

    def translate_google(self):
        try:
            output = self.tr.translate_google(self.input_text, self.lang)
        except requests.exceptions.ConnectionError:
            self.result.emit("Network error")
            return
        self.result.emit(output)

    def synonym(self):
        try:
            output = self.tr.synonym(self.input_text, self.lang)
        except requests.exceptions.ConnectionError:
            self.result.emit("Network error")
            return
        self.result.emit(output)

    def definition(self):
        try:
            output = self.tr.definition(self.input_text, self.lang)
        except requests.exceptions.ConnectionError:
            self.result.emit("Network error")
            return
        self.result.emit(output)

    def translate_yandex(self):
        try:
            output = self.tr.translate_yandex(self.input_text, self.lang)
        except requests.exceptions.ConnectionError:
            self.result.emit("Network error")
            return
        self.result.emit(output)

    def dictionary_yandex(self):
        try:
            output = self.tr.dictionary_yandex(self.input_text, self.lang)
        except requests.exceptions.ConnectionError:
            self.result.emit("Network error")
            return
        self.result.emit(output)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
