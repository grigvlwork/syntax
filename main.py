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
import shutil
import os
import glob
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from mainwindow import Ui_MainWindow
from need_file import Ui_need_file_dlg


def run_text(text, timeout):
    with open('code.py', 'w', encoding='utf-8') as c:
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


class Need_file_dlg(QDialog, Ui_need_file_dlg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('mainwindow.ui', self)
        self.setupUi(self)
        self.part_cb.setVisible(False)
        self.number_cb.setVisible(False)
        self.use_file_cb.setChecked(False)
        self.teacher_comment = ''
        self.correct_code = ''
        self.pupil_code = ''
        self.correct_code_model = QStandardItemModel()
        self.pupil_code_model = QStandardItemModel()
        self.tab_to_space_btn.clicked.connect(self.tab_to_space)
        self.explanation_pte.textChanged.connect(self.create_my_answer)
        self.insert_answer_btn.clicked.connect(self.insert)
        self.insert_code_btn.clicked.connect(self.insert_code)
        self.use_file_cb.clicked.connect(self.use_file)
        self.run_btn.clicked.connect(self.run_correct)
        self.pep8_btn.clicked.connect(self.pep8_correct)
        self.copy_to_correct_btn.clicked.connect(self.copy_to_correct)
        self.pupil_tw.currentChanged.connect(self.pupil_row_generator)
        self.correct_tw.currentChanged.connect(self.correct_row_generator)
        self.copy_answer_btn.clicked.connect(self.copy_my_answer)

    def insert(self):
        # self.curr_time = 0
        # self.working_clock.start()
        s = pyperclip.paste()
        # s = s.encode(encoding='UTF-8', errors='strict').decode()
        self.teacher_answer_pte.setPlainText(s)
        self.processing()
        self.part_cb.setVisible(False)
        self.number_cb.setVisible(False)
        self.use_file_cb.setChecked(False)

    def insert_code(self):
        t = pyperclip.paste()
        t = t.replace('```\n\n', '')
        t = t.replace('```\n', '')
        t = t.replace('```', '')
        self.pupil_code_pte.setPlainText(t)
        self.pupil_code = t
        self.copy_to_correct()
        self.run_correct()

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
            if self.teacher_comment == 'Комментарий к задаче для супертренера':
                self.teacher_comment = ''
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

    def run_correct(self):
        if self.use_file_cb.isChecked():
            if (self.part_cb.currentText() == 'beta' or
                    self.number_cb.currentText() in ['17', '22', '24']):
                folder = '/files/beta/'
            else:
                folder = '/files/' + self.part_cb.currentText() + '/'
            file_name = self.number_cb.currentText() + '.*'
            for file in glob.glob(os.getcwd() + folder + file_name):
                shutil.copy(file, os.getcwd())
        elif not self.use_file_cb.isChecked() and \
                ('.txt' in self.correct_code_pte.toPlainText() or
                 '.csv' in self.correct_code_pte.toPlainText()):
            need_file_frm = Need_file_dlg()
            need_file_frm.exec()
            if need_file_frm.accepted:
                if (need_file_frm.part_cb.currentText() == 'beta' or
                        need_file_frm.number_cb.currentText() in ['17', '22', '24']):
                    folder = '/files/beta/'
                else:
                    folder = '/files/' + need_file_frm.part_cb.currentText() + '/'
                file_name = need_file_frm.number_cb.currentText() + '.*'
                for file in glob.glob(os.getcwd() + folder + file_name):
                    shutil.copy(file, os.getcwd())
                self.use_file_cb.setChecked(True)
                self.part_cb.setVisible(True)
                self.part_cb.setCurrentText(need_file_frm.part_cb.currentText())
                self.number_cb.setVisible(True)
                self.number_cb.setCurrentText(need_file_frm.number_cb.currentText())
            else:
                return
        code = self.correct_code_pte.toPlainText()
        timeout = self.timeout_sb.value()
        self.correct_output_lb.setText('Вывод: ' + run_text(remove_comments(code), timeout))

    def pep8_correct(self):
        self.correct_code_pte.setPlainText(self.correct_code_pte.toPlainText().replace('\t', '    '))
        code = self.correct_code_pte.toPlainText()
        try:
            code = black.format_str(code, mode=black.Mode(
                target_versions={black.TargetVersion.PY310},
                line_length=101,
                string_normalization=False,
                is_pyi=False,
            ), )
        except Exception as err:
            code = code.strip()
        self.correct_code_pte.setPlainText(code)
        self.correct_code = code

    def copy_to_correct(self):
        self.correct_code_pte.clear()
        self.correct_code_pte.setPlainText(self.pupil_code_pte.toPlainText())

    def pupil_row_generator(self):
        if self.pupil_tw.currentIndex() == 1:
            self.pupil_code_model.clear()
            for row in self.pupil_code_pte.toPlainText().split('\n'):
                it = QStandardItem(row)
                self.pupil_code_model.appendRow(it)
            self.pupil_code_tv.setModel(self.pupil_code_model)
            self.pupil_code_tv.horizontalHeader().setVisible(False)
            self.pupil_code_tv.resizeColumnToContents(0)

    def correct_row_generator(self):
        if self.correct_tw.currentIndex() == 1:
            self.correct_code_model.clear()
            for row in self.correct_code_pte.toPlainText().split('\n'):
                it = QStandardItem(row)
                self.correct_code_model.appendRow(it)
            self.correct_code_tv.setModel(self.correct_code_model)
            self.correct_code_tv.horizontalHeader().setVisible(False)
            self.correct_code_tv.resizeColumnToContents(0)

    def tab_to_space(self):
        t = self.explanation_pte.toPlainText()
        if t.count('```') in [1, 2, 3]:
            t = t.replace('```\n\n', '')
            t = t.replace('```\n', '')
            t = t.replace('```', '')
        else:
            s = t.split('```\n')
            t = s[0] + '```\n'.join(s[1:-1]) + s[-1]
        self.explanation_pte.setPlainText(t)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    msg = QMessageBox.critical(
        None,
        "Error catched!:",
        tb
    )
    QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = excepthook
    ex.show()
    sys.exit(app.exec_())
