# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase
from applic_viewer import Applic_Viewer


class Applic_KNITU(object):
    db = None
    id = None
    centralWidget = None

    def get_connect(self):
        self.db = DataBase()
        self.answApplicContract = self.db.query(f'''SELECT *
            FROM applic_contract WHERE id = {self.id};''')[0]
        self.answContract = self.db.query(f'''SELECT *
            FROM contract WHERE id = {self.answApplicContract[3]}''')[0]
        self.answApplic = self.db.query(
            f'''SELECT id, name, date, (SELECT number FROM applic_contract
        WHERE id = applicat.applic_contract_id), status FROM applicat
        WHERE contract_id = {self.answApplicContract[3]} AND
        applicat.applic_contract_id = {self.id};''')
        self.answTypeResearch = self.db.query(f'''SELECT
        type_research, count_sample, deadline, price
        FROM types_of_research WHERE applic_contract_id = {self.id};''')

    def viewer(
          self, widget, btnHome, setupCentralWidget, btnBack, id):
        '''Отрисовка окна для просмотра Заявки по Договору'''
        self.id = id
        self.btnHome = btnHome
        self.btnBack = btnBack
        self.btnHome(widget)
        self.btnBack(widget)
        self.get_connect()
        self.setupCentralWidget = setupCentralWidget

        title = QtWidgets.QLabel(widget)
        title.setText(f'''         Заявка №{
            self.answApplicContract[1]} от {
                self.answApplicContract[2].strftime("%d.%m.%Y")
                } \nк Договору № {
                self.answContract[1]} от {
                self.answContract[3].strftime("%d.%m.%Y")}''')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setGeometry(QtCore.QRect(405, 40, 380, 50))

        statusLabel = QtWidgets.QLabel(widget)
        statusLabel.setGeometry(QtCore.QRect(550, 90, 100, 20))
        font = QtGui.QFont()
        font.setWeight(40)
        font.setItalic(True)
        statusLabel.setFont(font)
        if self.answApplicContract[6] == 2:
            statusLabel.setText('Выполнена')
            statusLabel.setStyleSheet('color: rgb(0, 128, 1)')
        if self.answApplicContract[6] == 1:
            statusLabel.setText('Активна')
            statusLabel.setStyleSheet('color: rgb(50, 0, 70)')
        if self.answApplicContract[6] == 0:
            statusLabel.setText('Аннулирована')
            statusLabel.setStyleSheet('color: rgb(139, 0, 0)')

        clientLabel = QtWidgets.QLabel(widget)
        clientLabel.setGeometry(QtCore.QRect(200, 110, 100, 20))
        clientLabel.setText('Заказчик')
        client = QtWidgets.QLineEdit(widget)
        client.setGeometry(QtCore.QRect(300, 110, 150, 20))
        client.setText(f'{self.answContract[2]}')

        tableApplicat = QtWidgets.QTableWidget(widget)
        tableApplicat.setGeometry(QtCore.QRect(250, 200, 500, 200))
        tableApplicat.setEditTriggers(
             QtWidgets.QAbstractItemView.NoEditTriggers)
        headApplic = ['№ Заявки', 'Дата',
                      'Заявка по \nДоговору', ' Статус']
        tableApplicat.setColumnCount(len(headApplic))
        tableApplicat.setRowCount(len(self.answApplic))
        tableApplicat.setHorizontalHeaderLabels(headApplic)
        tableApplicat.setSortingEnabled(True)
        tableApplicat.scrollToBottom()
        for i in range(len(self.answApplic)):
            for j in range(len(headApplic)):
                item = QtWidgets.QTableWidgetItem()
                tableApplicat.setItem(i, j, item)
                item = tableApplicat.item(i, j)
                item.setText(str(self.answApplic[i][j+1]))
                if j == 1:
                    val = str(self.answApplic[i][j+1]).split('-')
                    val = '.'.join(val[::-1])
                    item.setText(val)
                if j == 3:
                    if item.text() == '1':
                        val = 'Активна'
                        item.setText(val)
                    if item.text() == '0':
                        val = 'Аннулирована'
                        item.setText(val)
                    if item.text() == '2':
                        val = 'Выполнена'
                        item.setText(val)
        tableApplicat.cellDoubleClicked.connect(
            lambda: self.applView(tableApplicat.currentRow(),
                                  self.btnBackApplicContract))

        if len(self.answContract[1].split('-')) != 1:
            tableApplicat.setGeometry(QtCore.QRect(250, 470, 500, 200))
            tableTypesResearch = QtWidgets.QTableWidget(widget)
            tableTypesResearch.setGeometry(QtCore.QRect(150, 200, 700, 180))
            tableTypesResearch.setEditTriggers(
                 QtWidgets.QAbstractItemView.NoEditTriggers)
            headTypesResearch = ['Вид исследований', 'Количество \nпроб',
                                 'Сроки выполнения \nисследований',
                                 'Цена (с НДС), \nрублей ']
            tableTypesResearch.setColumnCount(len(headTypesResearch))
            tableTypesResearch.setRowCount(len(self.answTypeResearch))
            tableTypesResearch.setHorizontalHeaderLabels(headTypesResearch)
            tableTypesResearch.setColumnWidth(0, 180)
            tableTypesResearch.setColumnWidth(1, 100)
            tableTypesResearch.setColumnWidth(2, 150)
            tableTypesResearch.setColumnWidth(3, 130)
            for i in range(len(self.answTypeResearch)):
                for j in range(len(headTypesResearch)):
                    item = QtWidgets.QTableWidgetItem()
                    tableTypesResearch.setItem(i, j, item)
                    if j != 3:
                        item = tableTypesResearch.item(i, j)
                        item.setText(str(self.answTypeResearch[i][j]))
                    else:
                        item = tableTypesResearch.item(i, j)
                        item.setText('{0:,.2f}'.format(
                            self.answTypeResearch[i][j]).replace(
                                ',', ' ').replace('.', ','))

            priceLabel = QtWidgets.QLabel(widget)
            if self.answApplicContract[7] and self.answApplicContract[8]:
                priceLabel.setText(f'''ИТОГО: {
                '{0:,.2f}'.format(self.answApplicContract[7]).replace(
                    ',', ' ').replace('.', ',')
                } руб. в том числе НДС {
                    '{0:,.2f}'.format(self.answApplicContract[8]).replace(
                        ',', ' ').replace('.', ',')} руб.''')
            priceLabel.setGeometry(QtCore.QRect(230, 380, 400, 20))

        f = all([i[4] == 0 for i in self.answApplic])

        if f and self.answApplicContract[6] == 1:
            btn_null = QtWidgets.QPushButton(widget)
            btn_null.setGeometry(QtCore.QRect(485, 675, 100, 40))
            btn_null.setText('Аннулировать')
            btn_null.clicked.connect(
                lambda: self.null_applic_contract(
                    self.setupCentralWidget, widget, self.btnHome,
                    self.btnBack, self.id, self.answApplicContract[1],
                    self.answContract[1]))

        f1 = all([
            i[4] != 1 for i in self.answApplic]) and len(self.answApplic) != 0

        if f1 and f is False and self.answApplicContract[6] == 1:
            btn_close = QtWidgets.QPushButton(widget)
            btn_close.setGeometry(QtCore.QRect(485, 675, 100, 40))
            btn_close.setText('Сформировать \nАкт')
            btn_close.clicked.connect(
                lambda: self.close_applic_contract(self.setupCentralWidget,
                                                   widget,
                                                   self.answApplicContract[1],
                                                   self.answContract[1],
                                                   self.id))

    def btnBackApplicContract(self, widget):
        '''Кнопка возврата к обзору Заявок по Договору'''
        btnBack = QtWidgets.QPushButton(widget)
        btnBack.setGeometry(QtCore.QRect(20, 70, 100, 30))
        btnBack.setText('Назад')
        btnBack.clicked.connect(lambda: self.fnBkApplContract(widget))

    def fnBkApplContract(self, widget):
        widget.hide()
        new_widget = QtWidgets.QWidget()
        self.setupCentralWidget(new_widget)
        self.viewer(new_widget, self.btnHome, self.setupCentralWidget,
                    self.btnBack, self.id)
        new_widget.show()

    def applView(self, row, btnBack):
        self.centralWidget = QtWidgets.QWidget()
        self.setupCentralWidget(self.centralWidget)
        av = Applic_Viewer()
        idCurrentApplic = self.answApplic[row][0]
        av.viewer(
            self.centralWidget, self.setupCentralWidget, self.btnHome,
            btnBack, idCurrentApplic)

    def null_applic_contract(self, setupCentralWidget,
                             widget, btnHome, btnBack, id,
                             number, numberContract):
        '''Метод обнуления Заявки'''
        self.centralWidget = widget
        f = self.messWarning(number, numberContract, 'Аннулировать')
        if f:
            self.centralWidget.hide()
            self.centralWidget = QtWidgets.QWidget()
            setupCentralWidget(self.centralWidget)
            self.db.query_insert(f'''UPDATE applic_contract
            SET status = 0 WHERE id = {id};''')
            queryLog = f'''Аннулирована Заявка №{
                number} по Договору {numberContract}'''
            self.db.insert_log(queryLog)
            self.viewer(
                self.centralWidget, btnHome, setupCentralWidget, btnBack, id)
            self.centralWidget.show()

    def messWarning(self, number, numberContract, text):
        '''Метод, вызывающий окно предупреждения перед обнуленем Заявки'''
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(f'''{text} Заявку №{
            number} по Договору №{numberContract}''')
        msgBox.setWindowTitle(" ")
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        returnValue = msgBox.exec()
        return returnValue == QtWidgets.QMessageBox.Ok

    def readTxt(self):
        with open('parametres.txt', 'r', encoding='utf-8') as f:
            listParametres = f.readlines()
            self.dirApplic = listParametres[0]

    def close_applic_contract(self, setupCentralWidget, widget,
                              number, numberContract, id):
        self.centralWidget = widget
        f = self.messWarning(number, numberContract, 'Завершить')
        if f:
            self.centralWidget.hide()
            self.centralWidget = QtWidgets.QWidget()
            setupCentralWidget(self.centralWidget)
            self.db.query_insert(f'''UPDATE applic_contract
                SET status = 2, date_close = CURRENT_DATE
                WHERE id = {id};''')
            self.viewer(
                    self.centralWidget, self.btnHome,
                    self.setupCentralWidget, self.btnBack, self.id)
            self.centralWidget.show()
