import sys
import traceback
import subprocess
import pyperclip
import black
import sys
import re
import enchant
import difflib
import datetime
import time
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from mainwindow import Ui_MainWindow


def run_text(text, timeout):
    with open('code.py', 'w') as c:
        c.write(text)
    try:
        completed_process = subprocess.run(['python', 'code.py'], capture_output=True, text=True, timeout=timeout)
        if completed_process.returncode == 0:
            if len(completed_process.stdout) > 25:
                return completed_process.stdout[:25] + '..'
            else:
                return completed_process.stdout
        else:
            if len(completed_process.stderr) > 50:
                return completed_process.stderr[:50] + '\n' + completed_process.stderr[50:]
            else:
                return completed_process.stderr
    except subprocess.TimeoutExpired:
        return f'Программа выполнялась более {timeout} секунд'


def remove_comments(code):
    return re.sub(r'#.*', '', code)


def spell_check(text):
    rus_alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    words = []
    word = ''
    for c in text:
        if c.lower() in rus_alph:
            word += c
        else:
            if len(word) > 0:
                words.append(word)
                word = ''
    result = []
    dictionary = enchant.Dict("ru_RU")
    for w in words:
        if not dictionary.check(w):
            sim = dict()
            suggestions = set(dictionary.suggest(w))
            for word in suggestions:
                measure = difflib.SequenceMatcher(None, w, word).ratio()
                sim[measure] = word
            result.append([w, sim[max(sim.keys())]])
    return result


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('mainwindow.ui', self)
        self.setupUi(self)
        self.part_cb.setVisible(False)
        self.number_cb.setVisible(False)
        self.use_file_cb.setChecked(False)
        self.teacher_comment = ''
        self.insert_answer_btn.clicked.connect(self.insert)
        self.use_file_cb.clicked.connect(self.use_file)


    def insert(self):
        # self.curr_time = 0
        # self.working_clock.start()
        self.teacher_answer_pte.setPlainText(pyperclip.paste())
        self.processing()
        self.part_cb.setVisible(False)
        self.number_cb.setVisible(False)
        self.use_file_cb.setChecked(False)

    def create_my_answer(self):
        text = '<explanation>\n' + self.explanation_pte.toPlainText() + '\n</explanation>\n\n' + \
               '<comment>\n' + self.teacher_comment + '\n</comment>'
        self.my_answer_pte.clear()
        self.my_answer_pte.appendPlainText(text)

    def processing(self):
        t = self.teacher_answer_pte.toPlainText()
        self.teacher_comment = ''
        if all(x in t for x in ['<explanation>', '</explanation>']):
            code = t[t.find('<explanation>') + 13:t.find('</explanation>')]
            self.explanation_pte.clear()
            code = code.strip()
            self.explanation_pte.appendPlainText(code)
        if all(x in t for x in ['<comment>', '</comment>']):
            self.teacher_comment = t[t.find('<comment>') + 9:t.find('</comment>')].strip()
        self.create_my_answer()

    def use_file(self):
        if self.use_file_cb.isChecked():
            self.part_cb.setVisible(True)
            self.number_cb.setVisible(True)
        else:
            self.part_cb.setVisible(False)
            self.number_cb.setVisible(False)

    def copy_my_answer(self):
        errors = spell_check(self.explanation_pte.toPlainText())
        if len(errors) > 0:
            s = 'Обнаружены ошибки в тексте, всё равно скопировать?\n'
            for err in errors:
                s += err[0] + ':    ' + err[1] + '\n'
            message = QMessageBox.question(self, "Орфографические ошибки", s,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message == QMessageBox.Yes:
                pyperclip.copy(self.my_answer_pte.toPlainText())
        else:
            pyperclip.copy(self.my_answer_pte.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()


    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print(tb)

        msg = QMessageBox.critical(
            None,
            "Error catched!:",
            tb
        )
        QApplication.quit()


    sys.excepthook = excepthook
    ex.show()
    sys.exit(app.exec_())