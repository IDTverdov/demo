# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase
# from datetime import date
# import docx
# from docx.shared import Pt
# from docx.shared import Inches
# from docx.enum.text import WD_ALIGN_PARAGRAPH


class Ui_Report(object):
    db = None
    answ_rep = None
    id_report = None
    list_report = None
    id_answ = None
    fnBtnToApplic = None
    setDirReport = None

    def readTxt(self):
        with open('parametres.txt', 'r', encoding='utf-8') as f:
            listParametres = f.readlines()
            self.dirReport = listParametres[2]

    def get_connect(self):
        self.db = DataBase()

    def report(self, widget, fnBtnToApplic):
        self.fnBtnToApplic = fnBtnToApplic
        self.fnBtnToApplic(widget)
        # self.get_connect()
        self.readTxt()

        title_report = QtWidgets.QLabel(widget)
        title_report.setGeometry(QtCore.QRect(188, 40, 190, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title_report.setFont(font)
        title_report.setText("Создать Протокол")

        label_num_applicat = QtWidgets.QLabel(widget)
        label_num_applicat.setGeometry(QtCore.QRect(178, 90, 60, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        label_num_applicat.setFont(font)
        label_num_applicat.setText("№ Заявки ")

        btn_go = QtWidgets.QPushButton(widget)
        btn_go.setGeometry(QtCore.QRect(213, 130, 140, 30))
        btn_go.setText("Найти")
        # btn_go.clicked.connect(self.search)
        btn_go.setAutoDefault(True)

        self.line_num_applicat = QtWidgets.QLineEdit(widget)
        self.line_num_applicat.setGeometry(QtCore.QRect(248, 90, 70, 20))
        self.line_num_applicat.setText('')
        self.line_num_applicat.returnPressed.connect(btn_go.click)

        self.comboBox = QtWidgets.QComboBox(widget)
        self.comboBox.setGeometry(QtCore.QRect(213, 180, 140, 30))

        btn_dwld = QtWidgets.QPushButton(widget)
        btn_dwld.setGeometry(QtCore.QRect(213, 230, 140, 50))
        btn_dwld.setText("Сохранить Протокол")
        btn_dwld.clicked.connect(lambda: self.get_report())

        btnOpenFolder = QtWidgets.QPushButton(widget)
        btnOpenFolder.setGeometry(QtCore.QRect(213, 400, 140, 30))
        btnOpenFolder.setText('Открыть папку')
        btnOpenFolder.clicked.connect(
             lambda: os.system(f'explorer.exe {self.dirReport}'))

        self.mess_text = QtWidgets.QLabel(widget)
        self.mess_text.setGeometry(QtCore.QRect(207, 360, 200, 30))

        QtCore.QMetaObject.connectSlotsByName(widget)

    def search(self):
        self.get_connect()
        self.comboBox.clear()
        num_applicat = self.line_num_applicat.text()
        if num_applicat != '':
            query = f'''SELECT id, name FROM report
            WHERE name LIKE '{num_applicat}%' AND date is Null;'''
            self.answ_rep = self.db.query(query)

            self.list_report = []
            for i in self.answ_rep:
                self.list_report.append(i[1])
            self.comboBox.addItems(self.list_report)
        else:
            self.comboBox.clear()

    def get_report(self):
        if self.comboBox.currentIndex() != -1:
            # id_anws = self.comboBox.currentIndex()
            # id_report = self.answ_rep[id_anws][0]
            # self.draw_report(id_report)  # фунция составления файла .docx
            self.clear_fields()

    def clear_fields(self):
        self.line_num_applicat.setText('')
        self.comboBox.clear()
