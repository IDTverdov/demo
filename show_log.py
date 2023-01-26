from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase


class Log(object):
    db = None

    def get_connect(self):
        self.db = DataBase()

    def showLog(self, widget):
        # self.get_connect()
        title = QtWidgets.QLabel(widget)
        title.setGeometry(QtCore.QRect(450, 100, 300, 30))
        title.setText('Последние действия')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)

        # answ = self.db.query('''SELECT date_time, last_query
        # FROM logs_table;''')[::-1]
        table = QtWidgets.QTableWidget(widget)
        table.setGeometry(QtCore.QRect(50, 150, 970, 500))
        a = 0
        headList = ['Дата/Время', 'Действие']
        b = len(headList)
        table.setColumnCount(b)
        table.setRowCount(a)
        table.setHorizontalHeaderLabels(headList)
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 720)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        for i in range(a):
            item = QtWidgets.QTableWidgetItem()
            table.setItem(i, 0, item)
            item = table.item(i, 0)
            item = QtWidgets.QTableWidgetItem()
            table.setItem(i, 1, item)
            item = table.item(i, 1)
