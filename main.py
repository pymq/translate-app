import os
import sys
from typing import List

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction,
                             QDesktopWidget, QLineEdit, QSystemTrayIcon, QMenu,
                             QCompleter)
from requests.exceptions import ConnectionError

import mainwindow
from constants import LANGUAGES
from history import History
from translate import Translator


class CustomLineEdit(QLineEdit):
    pasted = pyqtSignal()
    up_pressed = pyqtSignal()
    down_pressed = pyqtSignal()

    def myPaste(self):
        self.paste()
        self.pasted.emit()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Up:
            self.up_pressed.emit()
        if QKeyEvent.key() == Qt.Key_Down:
            self.down_pressed.emit()
        super().keyPressEvent(QKeyEvent)


# noinspection PyArgumentList,PyUnresolvedReferences
class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        import module_locator
        self.module_path = module_locator.module_path()
        self.tr = Translator(os.path.join(self.module_path, 'config.ini'))
        self.history = History(os.path.join(self.module_path, 'history.txt'))
        self.threads = [None for _ in range(5)]
        self.setupUi(self)
        self.center()

        self.inputEdit.pasted.connect(self.translate)
        self.inputEdit.up_pressed.connect(self.navigate_history_forward)
        self.inputEdit.down_pressed.connect(self.navigate_history_backward)
        self.inputEdit.installEventFilter(self)

        self.actionExit = QAction('Exit', self, shortcut='Ctrl+Shift+Q', triggered=self.close)
        self.actionHideOrShow = QAction('Hide', self, shortcut='Ctrl+Q', triggered=self.hide_or_show)
        self.actionTranslate = QAction('Translate', self, triggered=self.translate)
        self.actionTranslate.setShortcuts([16777220, Qt.CTRL + Qt.Key_Space, Qt.Key_Enter])
        self.translateButton.pressed.connect(self.translate)
        self.actionSettings = QAction('Settings')
        selectInputAction = QAction('Focus input', self, shortcut='Ctrl+L', triggered=self.input_edit_set_focus)
        self.addAction(selectInputAction)

        self.tray = QSystemTrayIcon(QIcon(os.path.join(self.module_path, 'icon.png')), self)
        trayMenu = QMenu()
        trayMenu.addAction(self.actionHideOrShow)
        trayMenu.addAction(self.actionSettings)
        trayMenu.addAction(self.actionExit)
        self.tray.setContextMenu(trayMenu)
        self.tray.show()

        self.menuTranslator.addAction(self.actionTranslate)
        self.menuTranslator.addAction(self.actionHideOrShow)
        self.menuTranslator.addAction(self.actionExit)
        self.menuTranslator.addAction(self.actionSettings)
        self.menuBar.addAction(self.menuTranslator.menuAction())

        self.show()
        dictionary_path = os.path.join(self.module_path, 'dictionary.txt')
        if os.path.exists(dictionary_path):
            with open(dictionary_path, "r", encoding='utf-8', newline='') as f:
                lines_list = list(map(str.strip, f.readlines()))
            completer = QCompleter(lines_list, self.inputEdit)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.inputEdit.setCompleter(completer)

        self.swapLangsButton.setIcon(QIcon(os.path.join(self.module_path, 'arrowupdown.png')))
        self.swapLangsButton.pressed.connect(self.swap_languages)

        for code, name in LANGUAGES.items():
            self.fromComboBox.addItem(name, userData=code)
            self.toComboBox.addItem(name, userData=code)

    def swap_languages(self):
        index1 = self.fromComboBox.currentIndex()
        index2 = self.toComboBox.currentIndex()
        self.fromComboBox.setCurrentIndex(index2)
        self.toComboBox.setCurrentIndex(index1)

    def hide_or_show(self):
        if self.isHidden():
            self.actionHideOrShow.setText('Hide')
            self.show()
        else:
            self.actionHideOrShow.setText('Show')
            self.hide()

    def eventFilter(self, QObject, QEvent):
        if (QObject == self.inputEdit):
            if (QEvent.type() == QEvent.KeyPress):
                if (QEvent.matches(QKeySequence.Paste)):
                    self.inputEdit.myPaste()
                    self.inputEdit.completer().popup().hide()
                    return True
            return False
        else:
            return QMainWindow.eventFilter(QObject, QEvent)

    def navigate_history_backward(self):
        # key down is 16777237
        self.history.navigate_back()
        self.inputEdit.setText(self.history.current_word)
        self.inputEdit.selectAll()
        self.restore_translations()

    def navigate_history_forward(self):
        # key up is 16777235
        self.history.navigate_forward()
        self.inputEdit.setText(self.history.current_word)
        self.inputEdit.selectAll()
        self.restore_translations()

    def restore_translations(self):
        translations = self.history.current_word_translations
        if not translations:
            self.set_translations([''] * 5)
            return

        translations_list = []
        for i in range(1, 6):
            if i in translations:
                translations_list.append(translations[i])
            else:
                translations_list.append('')
        self.set_translations(translations_list)

    def set_translations(self, translations: List[str]):
        self.textEdit_1.setText(translations[0])
        self.textEdit_2.setText(translations[1])
        self.textEdit_3.setText(translations[2])
        self.textEdit_4.setText(translations[3])
        self.textEdit_5.setText(translations[4])

    @pyqtSlot()
    def translate(self):
        input_text = self.inputEdit.text().strip().lower()
        if not input_text:
            self.inputEdit.setText('')
            return
        en_alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                  'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        if self.autoDetectCheckBox.isChecked():
            if input_text[0] in en_alp or input_text[1] in en_alp:
                lang = 'en-ru'
            else:
                lang = 'ru-en'
            src, dest = lang.split('-')
            from_index = self.fromComboBox.findData(src)
            to_index = self.fromComboBox.findData(dest)
            self.fromComboBox.setCurrentIndex(from_index)
            self.toComboBox.setCurrentIndex(to_index)

        else:
            lang_from = self.fromComboBox.currentData()
            lang_to = self.toComboBox.currentData()
            lang = f'{lang_from}-{lang_to}'

        lst = [
            (self.tr.translate_google, self.textEdit_1, 1),
            (self.tr.translate_yandex, self.textEdit_2, 2),
            (self.tr.definition, self.textEdit_3, 3),
            (self.tr.dictionary_yandex, self.textEdit_4, 4),
            (self.tr.translate_multitran, self.textEdit_5, 5)
        ]
        for i, item in enumerate(lst):
            self.threads[i] = CustomThread(input_text, lang, item[0])
            self.threads[i].result.connect(self.set_text_decorator(item[1], item[2]))
            self.threads[i].finished.connect(self.threads[i].exit)
            self.threads[i].start()

        self.inputEdit.setText(input_text)
        self.input_edit_set_focus()
        self.history.append(input_text)

    def input_edit_set_focus(self):
        self.inputEdit.selectAll()
        self.inputEdit.setFocus()

    def set_text_decorator(self, textedit, number):
        @pyqtSlot(str, str)
        def set_text(translation, input_text):
            textedit.setText(translation)
            self.history.upload_word_translations(input_text, {number: translation})

        return set_text

    def closeEvent(self, QCloseEvent):
        self.history.save_history()
        super().closeEvent(QCloseEvent)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class CustomThread(QThread):
    result = pyqtSignal(str, str)

    def __init__(self, input_text, lang, func, parent=None):
        self.input_text = input_text
        self.lang = lang
        self.func = func
        super().__init__(parent)

    def run(self):
        try:
            output = self.func(self.input_text, self.lang)
        except ConnectionError:
            self.result.emit("Network error", self.input_text)
            return
        self.result.emit(output, self.input_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
