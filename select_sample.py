# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase


class Ui_Select_sample(object):
    db = None
    answ_samp = None
    cb = None

    def get_connect(self):
        self.db = DataBase()

    def get_samp(self):
        self.answ_samp = self.db.query('''SELECT id, number, name FROM sample
        WHERE applicat_id is Null;''')

    def select_sample(self, Dialog):
        # self.get_connect()
        Dialog.resize(700, 500)
        Dialog.setWindowTitle("Выбрать образцы")

        self.selectSamp_Label = QtWidgets.QLabel(Dialog)
        self.selectSamp_Label.setGeometry(QtCore.QRect(230, 10, 230, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.selectSamp_Label.setFont(font)
        self.selectSamp_Label.setText("Выбрать образцы")

        # Параметры таблицы
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(40, 70, 620, 330))
        # self.get_samp()
        # self.a_samp = len(self.answ_samp)
        self.a_samp = 0

        head_list_samp = ['Лабораторный номер',
                          'Наименование \nобразца Заказчика',
                          'Исследование']
        self.tableWidget.setColumnCount(len(head_list_samp))
        self.tableWidget.setRowCount(self.a_samp)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 120)
        self.tableWidget.scrollToBottom()
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        self.tableWidget.setHorizontalHeaderLabels(head_list_samp)

        # Чекбоксы!!!!

        for i in range(self.a_samp):
            for j in range(9):
                item = QtWidgets.QTableWidgetItem()
                if 0 <= j < 2:
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(self.answ_samp[i][j+1]))
                else:
                    self.tableWidget.setColumnWidth(j, 30)
                    widget = QtWidgets.QWidget()
                    checkbox = QtWidgets.QCheckBox()
                    layO = QtWidgets.QHBoxLayout(widget)
                    layO.setAlignment(QtCore.Qt.AlignCenter)
                    layO.addWidget(checkbox)
                    layO.setContentsMargins(0, 0, 0, 0)
                    self.tableWidget.setCellWidget(i, j, widget)

        # ОК/Отмена
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 420, 340, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(lambda: self.cb(self.get_save()))
        self.buttonBox.rejected.connect(Dialog.reject)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def setHandler(self, cb):
        self.cb = cb

    def get_save(self):
        checked = []
        for i in range(self.tableWidget.rowCount()):
            for j in range(2, 9):
                if self.tableWidget.cellWidget(i, j).findChild(
                           type(QtWidgets.QCheckBox())).isChecked():
                    my_tup = (self.answ_samp[i][0], j-1)
                    checked.append(my_tup)

        return checked
