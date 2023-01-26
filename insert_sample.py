# -*- coding: utf-8 -*-

# import pandas as pd
# from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase


class Ui_Insert_samples(object):
    fname = None
    fnBtnToApplic = None

    def get_connect(self):
        self.db = DataBase()
        self.db.connect()

    def insert_samples(self, widget, fnBtnToApplic):
        self.fnBtnToApplic = fnBtnToApplic
        self.fnBtnToApplic(widget)
        # self.get_connect()

        titleSample = QtWidgets.QLabel(widget)
        titleSample.setGeometry(QtCore.QRect(230, 40, 300, 30))
        titleSample.setText("Внести новые образцы")
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        titleSample.setFont(font)

        self.tableWidget = QtWidgets.QTableWidget(widget)
        self.tableWidget.setGeometry(QtCore.QRect(50, 90, 620, 150))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(4)
        header = ["Наименование пробы Заказчика",
                  "Описание пробы", "Примечания"]
        item = self.tableWidget.setHorizontalHeaderLabels(header)
        for i in range(4):
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, j, item)

        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(25)

        text_or = QtWidgets.QLabel(widget)
        text_or.setText('или')
        text_or.setGeometry(QtCore.QRect(346, 250, 18, 10))

        # Кнопка запуска обработчика
        btn_save = QtWidgets.QPushButton(widget)
        btn_save.setGeometry(QtCore.QRect(317, 350, 76, 25))
        btn_save.setText("Сохранить")
        btn_save.clicked.connect(lambda: self.saveSamples())

        # текстовое поле
        self.text_message = QtWidgets.QLabel(widget)

        # Кнопка загрузки проб из файла
        btn_import = QtWidgets.QPushButton(widget)
        btn_import.setGeometry(QtCore.QRect(280, 280, 150, 40))
        btn_import.setText("Внести образцы из файла")
        btn_import.clicked.connect(lambda: self.open_file())

        QtCore.QMetaObject.connectSlotsByName(widget)

    @QtCore.pyqtSlot()
    def open_file(self):
        fwin = QtWidgets.QMainWindow()
        self.fname = QtWidgets.QFileDialog.getOpenFileName(
            fwin, "Выбор файла", "C:/Users/Administrator/Documents",
            "Excel (*.xlsx)")[0]
        if self.fname == '':
            text = 'Файл не выбран'
        else:
            text = f'Выбран файл {self.fname}'
        self.text_message.setText(text)
        self.text_message.setGeometry(QtCore.QRect(100, 360, 510, 100))
        return self.fname

    # def saveSamples(self):
    #     self.get_connect()
    #     query = ('''INSERT INTO sample (number, name, type, info, date)
    #     VALUES (%s, %s, %s, %s, current_date)''')
    #     res = []
    #     if self.fname is None or self.fname == '':
    #         for i in range(4):
    #             tup = tuple()
    #             for j in range(3):
    #                 a = self.tableWidget.item(i, j).text()
    #                 tup += (a,)
    #             if tup == ('', '', ''):
    #                 continue
    #             else:
    #                 res.append(tup)
    #     else:
    #         xl = pd.read_excel(self.fname)
    #         s = xl.values
    #         for i in s:
    #             i = tuple(i)
    #             res.append(i)
    #     if res == []:
    #         self.text_message.setText('Внесите хотя бы один образец')
    #         self.text_message.setGeometry(QtCore.QRect(260, 360, 200, 100))
    #     else:
    #         last_num = self.db.query('''SELECT number FROM sample
    #         WHERE id = (SELECT MAX(id) FROM sample)''')
    #         last_date = self.db.query('''SELECT date FROM sample
    #         WHERE id = (SELECT MAX(id) FROM sample)''')
    #         date_now = datetime.now()
    #         date_now = str(datetime.date(date_now))[:4]

    #         if len(last_num) == 0 or str(last_date[0][0])[:4] != date_now:
    #             num = 1
    #         else:
    #             num = last_num[0][0]+1
    #         num_list = []

    #         for i in range(len(res)):
    #             tup = (num,)
    #             tup = tup + res[i]
    #             res[i] = tup
    #             num_list.append(num)
    #             num += 1

    #         for r in res:
    #             self.db.query_insert(query, r)

    #         if len(num_list) == 1:
    #             text = f'''               Сохранено
    #             \nЛабораторный номер: {num_list[0]}'''
    #             querylog = f'''Внесена проба №{num_list[0]}'''
    #         else:
    #             text = f'''                  Сохранено
    #             \nЛабораторные номера: {num_list[0]}-{num_list[-1]}'''
    #             querylog = f'Внесены пробы №{num_list[0]}-{num_list[-1]}'
    #         self.text_message.setText(text)
    #         self.text_message.setGeometry(QtCore.QRect(270, 360, 300, 100))
    #         self.db.insert_log(querylog)

    #         for i in range(4):
    #             for j in range(3):
    #                 item = QtWidgets.QTableWidgetItem()
    #                 self.tableWidget.setItem(i, j, item)
    #         self.fname = None
    #         res = []
    def saveSamples(self):
        self.text_message.setText('БД не подключена')
