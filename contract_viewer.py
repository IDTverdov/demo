# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase
from applic_knitu_viewer import Applic_KNITU


class ConactViewer(object):
    db = None

    def get_connect(self):
        self.db = DataBase()
        self.answContract = self.db.query(f'''SELECT * FROM contract
          WHERE id = {self.id};''')[0]
        self.answApplContr = self.db.query(f'''SELECT id, number, date, status
          FROM applic_contract WHERE contract_id = {self.id} ''')
        self.answSA = self.db.query(f'''SELECT num,  date_sa, date_new
        FROM `supplementary agreement` WHERE contract_id = {self.id};''')

    def viewer(
         self, widget, setupCentralWidget, btnHome, btnBack, id):
        '''Отрисовка окна для просмотра Договора'''
        self.id = id
        self.setupCentralWidget = setupCentralWidget
        self.btnHome = btnHome
        self.btnHome(widget)
        self.btnBackToSouce = btnBack
        self.btnBackToSouce(widget)

        self.get_connect()

        title = QtWidgets.QLabel(widget)
        if len(self.answContract[1].split('-')) == 1:
            title.setText(f'Договор №{self.answContract[1]} (НИР)')
        else:
            title.setText(f'Договор №{self.answContract[1]}')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setGeometry(QtCore.QRect(425, 40, 300, 30))

        clientLabel = QtWidgets.QLabel(widget)
        clientLabel.setGeometry(QtCore.QRect(200, 100, 50, 20))
        clientLabel.setText('Заказчик')
        clientLine = QtWidgets.QLineEdit(widget)
        clientLine.setGeometry(QtCore.QRect(260, 100, 600, 20))
        clientLine.setText(self.answContract[2])
        clientLine.setReadOnly(True)

        date = QtWidgets.QLabel(widget)
        date.setGeometry(QtCore.QRect(485, 70, 100, 20))
        dateValue = '.'.join((str(self.answContract[3]).split('-'))[::-1])
        date.setText(f'от {dateValue}')

        dateEndLabel = QtWidgets.QLabel(widget)
        dateEndLabel.setGeometry(QtCore.QRect(110, 130, 150, 20))
        dateEndLabel.setText('Дата окончания Договора')
        dateEnd = QtWidgets.QLineEdit(widget)
        dateEnd.setGeometry(QtCore.QRect(260, 130, 600, 20))
        dateValueEnd = '.'.join((str(self.answContract[4]).split('-'))[::-1])
        dateEnd.setText(dateValueEnd)
        dateEnd.setReadOnly(True)

        adressLabel = QtWidgets.QLabel(widget)
        adressLabel.setGeometry(QtCore.QRect(160, 160, 90, 20))
        adressLabel.setText('Адрес Заказчика')
        adressLine = QtWidgets.QLineEdit(widget)
        adressLine.setGeometry(QtCore.QRect(260, 160, 600, 20))
        adressLine.setText(self.answContract[5])
        adressLine.setReadOnly(True)

        phoneLabel = QtWidgets.QLabel(widget)
        phoneLabel.setGeometry(QtCore.QRect(135, 190, 120, 20))
        phoneLabel.setText('Контактный телефон')
        phoneLine = QtWidgets.QLineEdit(widget)
        phoneLine.setGeometry(QtCore.QRect(260, 190, 200, 20))
        phoneLine.setText(self.answContract[6])
        phoneLine.setReadOnly(True)

        labelContrApplicat = QtWidgets.QLabel(widget)
        labelContrApplicat.setGeometry(QtCore.QRect(445, 250, 200, 30))
        labelContrApplicat.setText('Заявки по Договору')
        f = QtGui.QFont()
        f.setBold(True)
        labelContrApplicat.setFont(f)
        tableContrApplicat = QtWidgets.QTableWidget(widget)
        tableContrApplicat.setGeometry(QtCore.QRect(300, 280, 400, 150))
        tableContrApplicat.setEditTriggers(
             QtWidgets.QAbstractItemView.NoEditTriggers)
        headApplic = ['№', 'Дата', 'Статус']
        tableContrApplicat.setColumnCount(len(headApplic))
        tableContrApplicat.setRowCount(len(self.answApplContr))
        tableContrApplicat.setHorizontalHeaderLabels(headApplic)
        for i in range(len(self.answApplContr)):
            for j in range(len(headApplic)):
                item = QtWidgets.QTableWidgetItem()
                if j == 1:
                    item.setText(
                        f'{self.answApplContr[i][j+1].strftime("%d.%m.%Y")}')
                else:
                    item.setText(f'{self.answApplContr[i][j+1]}')
                if j == 2:
                    if self.answApplContr[i][j+1] == 1:
                        item.setText('Активна')
                    if self.answApplContr[i][j+1] == 2:
                        item.setText('Выполнена')
                    if self.answApplContr[i][j+1] == 0:
                        item.setText('Аннулирована')
                tableContrApplicat.setItem(i, j, item)
        tableContrApplicat.doubleClicked.connect(
            lambda: self.applic_contract_view(tableContrApplicat.currentRow()))

        if len(self.answContract[1].split('-')) != 1:
            labelContrApplicat.setGeometry(QtCore.QRect(205, 220, 200, 30))
            tableContrApplicat.setGeometry(QtCore.QRect(50, 250, 400, 150))
            labelSA = QtWidgets.QLabel(widget)
            labelSA.setGeometry(QtCore.QRect(730, 320, 200, 30))
            labelSA.setText('Дополнительные соглашения')
            labelSA.setFont(f)
            tableSA = QtWidgets.QTableWidget(widget)
            tableSA.setGeometry(QtCore.QRect(650, 350, 380, 250))
            tableSA.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            headSA = ['Номер \nДополнительного \nСоглашения',
                      'Дата \nДополнительного \nСоглашения',
                      'Дата \nокончания \nДоговора']
            tableSA.setColumnCount(len(headSA))
            tableSA.setColumnWidth(0, 120)
            tableSA.setColumnWidth(1, 120)
            tableSA.setRowCount(len(self.answSA))
            tableSA.setHorizontalHeaderLabels(headSA)
            for i in range(len(self.answSA)):
                for j in range(len(headSA)):
                    item = QtWidgets.QTableWidgetItem()
                    tableSA.setItem(i, j, item)
                    item = tableSA.item(i, j)
                    item.setText(str(self.answSA[i][j]))
                    if j > 0:
                        val = str(self.answSA[i][j]).split('-')
                        val = '.'.join(val[::-1])
                        item.setText(val)

            btnSA = QtWidgets.QPushButton(widget)
            btnSA.setGeometry(QtCore.QRect(770, 620, 140, 30))
            btnSA.setText('Внести дополнительное \nсоглашение')
            btnSA.clicked.connect(lambda: self.showNewSA(self.id, widget))

            requsiteLabel = QtWidgets.QLabel(widget)
            requsiteLabel.setGeometry(QtCore.QRect(220, 425, 100, 20))
            requsiteLabel.setText('Реквизиты')
            f = QtGui.QFont()
            f.setBold(True)
            requsiteLabel.setFont(f)
            requsiteText = QtWidgets.QTextEdit(widget)
            requsiteText.setGeometry(QtCore.QRect(100, 445, 300, 230))
            requsiteText.setText(self.answContract[8])
            requsiteText.setReadOnly(True)

    def btnBackContract(self, widget):
        '''Кнопка "Назад" к Договорам'''
        btnBack = QtWidgets.QPushButton(widget)
        btnBack.setGeometry(QtCore.QRect(20, 70, 100, 30))
        btnBack.setText('Назад')
        btnBack.clicked.connect(lambda: self.fnBkContract(widget))

    def fnBkContract(self, widget):
        widget.hide()
        new_widget = QtWidgets.QWidget()
        self.setupCentralWidget(new_widget)
        self.viewer(new_widget, self.setupCentralWidget,
                    self.btnHome, self.btnBackToSouce, self.id)
        new_widget.show()

    def newSA(self, widget, setupCentralWidget, btnHome, btnBack, id):
        '''Новое допсоглашение'''
        self.id = id
        self.setupCentralWidget = setupCentralWidget
        self.btnHome = btnHome
        self.btnHome(widget)
        btnBack(widget)

        self.get_connect()

        title = QtWidgets.QLabel(widget)
        title.setText(
            f'''Дополнительное соглашение \n      к Договору №{
                self.answContract[1]}''')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setGeometry(QtCore.QRect(400, 40, 310, 60))

        date = QtWidgets.QLabel(widget)
        date.setGeometry(QtCore.QRect(510, 90, 100, 20))
        dateValue = '.'.join((str(self.answContract[3]).split('-'))[::-1])
        date.setText(f'от {dateValue}')

        numberLabel = QtWidgets.QLabel(widget)
        numberLabel.setGeometry(QtCore.QRect(200, 200, 200, 20))
        numberLabel.setText('Номер Дополнительного Соглашения')
        self.number = QtWidgets.QLineEdit(widget)
        self.number.setGeometry(QtCore.QRect(400, 200, 300, 20))
        self.number.setText('')

        dateLabel = QtWidgets.QLabel(widget)
        dateLabel.setGeometry(QtCore.QRect(140, 250, 250, 20))
        dateLabel.setText('Дата заключения Дополнительного Соглашения')
        self.date = QtWidgets.QDateEdit(widget)
        self.date.setGeometry(QtCore.QRect(400, 250, 300, 20))
        self.date.setDisplayFormat('dd.MM.yyyy')

        dateNewLabel = QtWidgets.QLabel(widget)
        dateNewLabel.setGeometry(QtCore.QRect(140, 300, 250, 20))
        dateNewLabel.setText('Обновлённая дата окончания Договора')
        self.dateNew = QtWidgets.QDateEdit(widget)
        self.dateNew.setGeometry(QtCore.QRect(400, 300, 300, 20))
        self.dateNew.setDisplayFormat('dd.MM.yyyy')

        btnSave = QtWidgets.QPushButton(widget)
        btnSave.setGeometry(QtCore.QRect(400, 350, 100, 30))
        btnSave.setText('Сохранить')
        btnSave.clicked.connect(self.saveSa)

        self.textMess = QtWidgets.QLabel(widget)
        self.textMess.setGeometry(QtCore.QRect(350, 450, 300, 40))

    def saveSa(self):
        number = self.number.text().strip()
        date = self.date.text().strip().split('.')
        date = '-'.join(date[::-1])
        dateNew = self.dateNew.text().strip().split('.')
        dateNew = '-'.join(dateNew[::-1])

        if number == '':
            self.textMess.setText(
                '            Не введён номер \nДополнительного Соглашения')
        elif date == '2000-01-01':
            self.textMess.setText(
                ' Не введёна дата заключения\nДополнительного Соглашения')
        elif dateNew == '2000-01-01':
            self.textMess.setText(
                'Не введёна обновлённая дата \n        окончания Договора')

        else:
            dateOld = self.answContract[4]
            query = '''INSERT INTO `supplementary agreement`
            (num, date_sa, date_old, date_new, contract_id)
            VALUES (%s, %s, %s, %s, %s);'''
            val = (str(number), str(date),
                   str(dateOld), str(dateNew), str(self.id))
            self.db.query_insert(query, val)
            query = "UPDATE contract SET date_end = %s WHERE id = %s"
            val = (dateNew, self.id)
            self.db.query_insert(query, val)
            queryLog = f'''Добавлено дополнительное соглашение
            №{number} к Договору №{self.answContract[1]}'''
            self.db.insert_log(queryLog)
            self.textMess.setText(f'''Добавлено дополнительное соглашение №{number}
            \n                 к Договору №{self.answContract[1]}''')
            self.number.setText('')
            self.date.setDate(QtCore.QDate(2000, 1, 1))
            self.dateNew.setDate(QtCore.QDate(2000, 1, 1))

    def showNewSA(self, id_contract, widget):
        widget.hide()
        new_widget = QtWidgets.QWidget()
        self.setupCentralWidget(new_widget)
        self.newSA(
            new_widget, self.setupCentralWidget,
            self.btnHome, self.btnBackContract, id_contract)

    def applic_contract_view(self, row):
        self.centralWidget = QtWidgets.QWidget()
        self.setupCentralWidget(self.centralWidget)
        acw = Applic_KNITU()
        id = self.answApplContr[row][0]
        acw.viewer(self.centralWidget, self.btnHome, self.setupCentralWidget,
                   self.btnBackContract, id)
