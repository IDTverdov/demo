# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase
from connect.mail import Set_Mail


class Applic_Viewer:
    db = None
    id_applic = None
    btnHome = None

    def get_connect(self):
        self.db = DataBase()
        self.answApplic = self.db.query(
            f'''SELECT * FROM applicat WHERE id = {self.id_applic};''')[0]
        self.answContract = self.db.query(f''' SELECT *
        FROM contract WHERE id = {self.answApplic[4]};''')[0]
        self.answReport = self.db.query(f'''SELECT report.name,
        IF(report.date IS NULL, 'В работе', report.date),
        IF(type_work IS NULL, '', type_work),
        GROUP_CONCAT(DISTINCT sample.number ORDER BY 1 SEPARATOR ', ')
        FROM report
        JOIN applicat ON applicat.id = applicat_id
        JOIN sample ON applicat.id = sample.applicat_id
        JOIN sample_has_method ON sample_id = sample.id
        JOIN method on method.id = sample_has_method.method_id
        WHERE applicat.id = {self.id_applic}
        AND sample_has_method.method_id = report.method_id
        GROUP BY report.name;''')
        self.answUsr = self.db.query(
            f'''SELECT GROUP_CONCAT(DISTINCT user.name ORDER BY 1 SEPARATOR '\n')
        FROM user_has_type_method
        INNER JOIN user ON user.id = user_has_type_method.user_id
        INNER JOIN type_method
            ON user_has_type_method.type_method_id = type_method.id
        INNER JOIN method
            ON type_method.method_id = method.id
        INNER JOIN applicat_has_uhtm ON
            applicat_has_uhtm.user_has_type_method_id = user_has_type_method.id
        WHERE applicat_id = {self.id_applic}
        GROUP BY method.id ORDER BY method.log;''')
        self.answApplicContract = self.db.query(
            f''' SELECT * FROM applic_contract
            WHERE id = {self.answApplic[3]}''')[0]
        self.answSample = self.db.query(f'''SELECT * FROM sample
            WHERE applicat_id = {self.id_applic}''')
        self.answDateReport = self.db.query(f'''SELECT date FROM report
            WHERE applicat_id = {self.id_applic}''')

    def viewer(self, widget, setupCentralWidget, btnHome, btnBack, id):
        '''Основной метод, открывающий окно просмотра Заявки'''
        self.id_applic = id
        self.btnHome = btnHome
        btnHome(widget)
        btnBack(widget)

        self.get_connect()

        title = QtWidgets.QLabel(widget)
        title.setText(f'Заявка №{self.answApplic[1]}')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setGeometry(QtCore.QRect(425, 40, 300, 30))

        date = QtWidgets.QLabel(widget)
        date.setGeometry(QtCore.QRect(485, 70, 100, 20))
        dateValue = '.'.join((str(self.answApplic[2]).split('-'))[::-1])
        date.setText('от ' + dateValue)

        statusLabel = QtWidgets.QLabel(widget)
        statusLabel.setGeometry(QtCore.QRect(495, 20, 100, 20))
        font = QtGui.QFont()
        font.setWeight(40)
        font.setItalic(True)
        statusLabel.setFont(font)
        if self.answApplic[6] == 2:
            statusLabel.setText('Выполнена')
            statusLabel.setStyleSheet('color: rgb(0, 128, 1)')
        if self.answApplic[6] == 1:
            statusLabel.setText('Активна')
            statusLabel.setStyleSheet('color: rgb(50, 0, 70)')
        if self.answApplic[6] == 0:
            statusLabel.setText('Аннулирована')
            statusLabel.setStyleSheet('color: rgb(139, 0, 0)')

        clientLabel = QtWidgets.QLabel(widget)
        clientLabel.setGeometry(QtCore.QRect(200, 100, 50, 20))
        clientLabel.setText('Заказчик')
        clientLine = QtWidgets.QLineEdit(widget)
        clientLine.setGeometry(QtCore.QRect(260, 100, 400, 20))
        clientLine.setText(self.answContract[2])
        clientLine.setReadOnly(True)

        adressLabel = QtWidgets.QLabel(widget)
        adressLabel.setGeometry(QtCore.QRect(160, 130, 90, 20))
        adressLabel.setText('Адрес Заказчика')
        adressLine = QtWidgets.QLineEdit(widget)
        adressLine.setGeometry(QtCore.QRect(260, 130, 400, 20))
        adressLine.setText(self.answContract[5])
        adressLine.setReadOnly(True)

        phoneLabel = QtWidgets.QLabel(widget)
        phoneLabel.setGeometry(QtCore.QRect(135, 160, 120, 20))
        phoneLabel.setText('Контактный телефон')
        phoneLine = QtWidgets.QLineEdit(widget)
        phoneLine.setGeometry(QtCore.QRect(260, 160, 200, 20))
        phoneLine.setText(self.answContract[6])
        phoneLine.setReadOnly(True)

        contractLabel = QtWidgets.QLabel(widget)
        contractLabel.setGeometry(QtCore.QRect(730, 100, 90, 20))
        contractLabel.setText('Номер Договора')
        contractLine = QtWidgets.QLineEdit(widget)
        contractLine.setGeometry(QtCore.QRect(820, 100, 100, 20))
        if len(self.answContract[1].split('-')) == 1:
            contractLine.setText('НИР')
        else:
            contractLine.setText(self.answContract[1])
        contractLine.setReadOnly(True)

        applicContractLabel = QtWidgets.QLabel(widget)
        applicContractLabel.setGeometry(QtCore.QRect(680, 130, 140, 20))
        applicContractLabel.setText('Номер Заявки по Договору')
        applicContractLine = QtWidgets.QLineEdit(widget)
        applicContractLine.setGeometry(QtCore.QRect(820, 130, 100, 20))
        applicContractLine.setText(str(self.answApplicContract[1]))
        applicContractLine.setReadOnly(True)

        line = QtWidgets.QFrame(widget)
        line.setGeometry(QtCore.QRect(430, 200, 150, 1))
        line.setFrameStyle(2)

        infoLabel = QtWidgets.QLabel(widget)
        infoLabel.setGeometry(QtCore.QRect(810, 450, 100, 20))
        infoLabel.setText('Примечания')
        f = QtGui.QFont()
        f.setBold(True)
        infoLabel.setFont(f)
        infoText = QtWidgets.QTextEdit(widget)
        infoText.setGeometry(QtCore.QRect(700, 475, 300, 170))
        infoText.setText(self.answApplic[5])
        infoText.setReadOnly(True)

        tableReport = QtWidgets.QTableWidget(widget)
        tableReport.setGeometry(QtCore.QRect(50, 220, 950, 205))
        tableReport.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tableReport.setRowCount(len(self.answReport))
        headListReport = ['№ Протокола', 'Дата выдачи/\n Стасус', 'Виды работ',
                          'Лабораторные\nномера проб', 'Исполнители']
        tableReport.setColumnCount(5)
        tableReport.setColumnWidth(2, 300)
        tableReport.setColumnWidth(4, 300)
        tableReport.setHorizontalHeaderLabels(headListReport)
        for i in range(len(self.answReport)):
            tableReport.setRowHeight(i, 50)
            for j in range(5):
                if j < 4:
                    item = QtWidgets.QTableWidgetItem()
                    tableReport.setItem(i, j, item)
                    item = tableReport.item(i, j)
                    item.setText(str(self.answReport[i][j]))
                if j == 1:
                    val = str(self.answReport[i][j]).split('-')
                    val = '.'.join(val[::-1])
                    item.setText(val)
                if j == 4:
                    item = QtWidgets.QTableWidgetItem()
                    tableReport.setItem(i, j, item)
                    item = tableReport.item(i, j)
                    item.setText(str(self.answUsr[i][0]))

        labelSample = QtWidgets.QLabel(widget)
        labelSample.setText('Опись проб')
        labelSample.setFont(f)
        labelSample.setGeometry(QtCore.QRect(300, 450, 100, 20))
        tableSample = QtWidgets.QTableWidget(widget)
        tableSample.setGeometry(QtCore.QRect(50, 475, 600, 170))
        tableSample.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tableSample.setRowCount(len(self.answSample))
        tableSample.setColumnCount(5)
        headListSample = ['Лабораторный \nномер', 'Наименование \nпробы',
                          'Описание пробы', 'Примечания', 'Дата приёма']
        tableSample.setHorizontalHeaderLabels(headListSample)
        for i in range(len(self.answSample)):
            for j in range(1, 6):
                item = QtWidgets.QTableWidgetItem()
                tableSample.setItem(i, j-1, item)
                item = tableSample.item(i, j-1)
                item.setText(str(self.answSample[i][j]))
                if j == 5:
                    val = str(self.answSample[i][j]).split('-')
                    val = '.'.join(val[::-1])
                    item.setText(val)
        tableSample.setColumnWidth(3, 140)
        tableSample.setColumnWidth(2, 110)

        f = all([True if i[0] is None else False for i in self.answDateReport])
        if f and self.answApplic[6] != 0:
            btn_null = QtWidgets.QPushButton(widget)
            btn_null.setGeometry(QtCore.QRect(485, 670, 100, 40))
            btn_null.setText('Аннулировать \nЗаявку')
            btn_null.clicked.connect(
                lambda: self.null_applicat(setupCentralWidget, widget, btnHome,
                                           btnBack, id, self.answApplic[1]))

    def null_applicat(self, setupCentralWidget,
                      widget, btnHome, btnBack, id, number):
        '''Метод обнуления Заявки'''
        self.centralWidget = widget
        f = self.messWarning(number)
        if f:
            self.centralWidget.hide()
            self.centralWidget = QtWidgets.QWidget()
            setupCentralWidget(self.centralWidget)
            self.db.query_insert(f'''UPDATE applicat
            SET status = 0 WHERE id = {id};''')
            queryLog = f'Аннулирована Заявка №{number}'
            self.db.query_insert(f'''UPDATE report SET date = current_date
            WHERE applicat_id = {id};''')
            self.db.insert_log(queryLog)
            self.viewer(
                self.centralWidget, setupCentralWidget, btnHome, btnBack, id)
            self.centralWidget.show()
            self.sendMail(id, number)

    def messWarning(self, number):
        '''Метод, вызывающий окно предупреждения перед обнуленем Заявки'''
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(f"Аннулировать Заявку №{number}")
        msgBox.setWindowTitle("")
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        returnValue = msgBox.exec()
        return returnValue == QtWidgets.QMessageBox.Ok

    def sendMail(self, id, number):
        '''Оптправляем письма исполнителям
        с оповещением аннулирования Заявки'''
        mail = Set_Mail()
        subject = f'Аннулирование Заявки №{number}'
        ids_usr = self.db.query(f'''SELECT user_id
        FROM user_has_type_method
        INNER JOIN applicat_has_uhtm ON
            user_has_type_method.id = applicat_has_uhtm.user_has_type_method_id
        WHERE applicat_id = {id}''')
        ids_usr = [str(ids_usr[i][0]) for i in range(len(ids_usr))]
        email_list = self.db.query(f'''SELECT email FROM user
            WHERE id IN ({','.join(ids_usr)});''')
        email_list = [email_list[i][0] for i in range(len(email_list))]

        text = f'''Добрый день! <br>Не нужно отвечать на данное сообщение. <br>
        Вы получили данное сообщение, так как
        Вы являетесь исполнителем Заявки №{number}. <br>Сообщаем, что данная
        Заявка аннулирована и работы по ней отменены.'''
        mail.sendMail(subject, email_list, text)
