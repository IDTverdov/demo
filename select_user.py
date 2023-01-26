# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase


class Ui_Select_user(object):
    db = None
    answ_uhtm = None
    mb = None
    cb = None

    def get_connect(self):
        self.db = DataBase()

    def setView(self, mb):
        self.mb = mb

    def select_user(self, Dialog):
        # self.get_connect()

        Dialog.resize(600, 400)
        Dialog.setWindowTitle("Выбрать исполнителей")

        self.selectUser_Label = QtWidgets.QLabel(Dialog)
        self.selectUser_Label.setGeometry(QtCore.QRect(170, 10, 230, 30))
        self.selectUser_Label.setText("Выбрать исполнителя")
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.selectUser_Label.setFont(font)

        if self.mb is None or self.mb == []:
            self.text_message = QtWidgets.QLabel(Dialog)
            self.text_message.setText('Сначала выберете пробы')
            self.text_message.setGeometry(QtCore.QRect(230, 155, 200, 20))

        else:
            # Формирование таблицы
            if len(self.mb) != 1:
                self.mb = tuple(self.mb)
            else:
                self.mb = f'({self.mb[0]})'
            self.tableWidget = QtWidgets.QTableWidget(Dialog)
            self.tableWidget.setGeometry(QtCore.QRect(30, 50, 540, 300))
            self.answ_uhtm = self.db.query(f'''SELECT user_has_type_method.id,
            type_method.name, (SELECT name FROM method
            WHERE id = type_method.method_id),
            (SELECT name FROM user WHERE id = user_has_type_method.user_id)
            FROM type_method
            INNER JOIN user_has_type_method ON
            type_method.id = user_has_type_method.type_method_id
            WHERE method_id IN {self.mb}
            ORDER BY 3;''')

            self.tableWidget.setColumnCount(4)
            a_uhtm = len(self.answ_uhtm)
            self.tableWidget.setRowCount(a_uhtm)
            head_list_usr = ['Метод', 'Анализ', 'ФИО Исполнителя', '']
            self.tableWidget.setHorizontalHeaderLabels(head_list_usr)
            self.tableWidget.setColumnWidth(2, 250)
            self.tableWidget.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)

            for i in range(a_uhtm):
                for j in range(4):
                    item = QtWidgets.QTableWidgetItem()
                    if 0 <= j < 3:
                        self.tableWidget.setItem(i, j, item)
                        item = self.tableWidget.item(i, j)
                        item.setText(str(self.answ_uhtm[i][j+1]))
                    else:
                        self.tableWidget.setColumnWidth(j, 30)
                        widget = QtWidgets.QWidget()
                        checkbox = QtWidgets.QCheckBox()
                        layO = QtWidgets.QHBoxLayout(widget)
                        layO.setAlignment(QtCore.Qt.AlignCenter)
                        layO.addWidget(checkbox)
                        layO.setContentsMargins(0, 0, 0, 0)
                        self.tableWidget.setCellWidget(i, j, widget)

        # Кнопки ок/отмена
        buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        buttonBox.setGeometry(QtCore.QRect(200, 360, 170, 32))
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(lambda: self.cb(self.get_save(Dialog)))
        buttonBox.rejected.connect(Dialog.reject)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def setHandler(self, cb):
        self.cb = cb

    def get_save(self, Dialog):
        if self.mb == () or self.mb is None:
            Dialog.close()

        else:
            checked = []
            for i in range(self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(i, 3).findChild(
                          type(QtWidgets.QCheckBox())).isChecked():
                    checked.append(self.answ_uhtm[i][0])
            return checked
