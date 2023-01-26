import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase


class Applic_KNITU(object):
    fnBtnToApplic = None

    def get_connect(self):
        self.db = DataBase()
        self.db.connect()

    def applic_knitu(self, widget, fnBtnToApplic):
        self.fnBtnToApplic = fnBtnToApplic
        self.fnBtnToApplic(widget)
        # self.get_connect()

        conractTitle = QtWidgets.QLabel(widget)
        conractTitle.setGeometry(QtCore.QRect(245, 40, 210, 30))
        conractTitle.setText("Заявка по Договору")
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        conractTitle.setFont(font)

        clientLabel = QtWidgets.QLabel(widget)
        clientLabel.setGeometry(QtCore.QRect(130, 80, 120, 20))
        clientLabel.setText(" Договор/Заказчик")
        self.line_client = QtWidgets.QLineEdit(widget)
        self.line_client.setGeometry(QtCore.QRect(240, 80, 160, 20))
        # self.line_client.returnPressed.connect(lambda: self.searchClients())
        self.comboBox = QtWidgets.QComboBox(widget)
        self.comboBox.setGeometry(QtCore.QRect(410, 80, 200, 20))

        labelNumber = QtWidgets.QLabel(widget)
        labelNumber.setGeometry(QtCore.QRect(80, 110, 200, 20))
        labelNumber.setText('Номер Заявки по Договору')
        self.lineNumber = QtWidgets.QLineEdit(widget)
        self.lineNumber.setGeometry(QtCore.QRect(230, 110, 100, 20))

        labelDate = QtWidgets.QLabel(widget)
        labelDate.setGeometry(QtCore.QRect(370, 110, 200, 20))
        labelDate.setText('  Дата Заявки по Договору')
        self.lineDate = QtWidgets.QDateEdit(widget)
        self.lineDate.setGeometry(QtCore.QRect(510, 110, 100, 20))
        self.lineDate.setDisplayFormat('dd.MM.yyyy')

        labelSampleRP = QtWidgets.QLabel(widget)
        labelSampleRP.setText('Необходимо провести исследования')
        labelSampleRP.setGeometry(QtCore.QRect(80, 140, 200, 20))
        self.lineSampleRP = QtWidgets.QLineEdit(widget)
        self.lineSampleRP.setGeometry(QtCore.QRect(270, 140, 200, 20))
        labelSampleRPInfo = QtWidgets.QLabel(widget)
        labelSampleRPInfo.setGeometry(QtCore.QRect(475, 140, 300, 20))
        labelSampleRPInfo.setText(
            '(указать объект исследования в родительном падеже)')
        f = QtGui.QFont()
        f.setItalic(True)
        labelSampleRPInfo.setFont(f)

        labelTarget = QtWidgets.QLabel(widget)
        labelTarget.setText('Целью исследований является определение')
        labelTarget.setGeometry(QtCore.QRect(80, 170, 240, 20))
        self.lineTarget = QtWidgets.QLineEdit(widget)
        self.lineTarget.setGeometry(QtCore.QRect(320, 170, 200, 20))
        labelTargetInfo = QtWidgets.QLabel(widget)
        labelTargetInfo.setGeometry(QtCore.QRect(525, 170, 300, 20))
        labelTargetInfo.setText(
            '(указать цель в родительном падеже)')
        labelTargetInfo.setFont(f)

        self.tableTypesResearch = QtWidgets.QTableWidget(widget)
        self.tableTypesResearch.setGeometry(QtCore.QRect(80, 200, 610, 180))
        headTypesResearch = ['Вид исследований', 'Количество \nпроб',
                             'Сроки выполнения \nисследований',
                             'Стоимость (с НДС), \nрублей ']
        self.tableTypesResearch.setColumnCount(len(headTypesResearch))
        self.tableTypesResearch.setRowCount(15)
        for i in range(15):
            for j in range(len(headTypesResearch)):
                item = QtWidgets.QTableWidgetItem()
                self.tableTypesResearch.setItem(i, j, item)
        self.tableTypesResearch.setHorizontalHeaderLabels(headTypesResearch)
        self.tableTypesResearch.setColumnWidth(0, 180)
        self.tableTypesResearch.setColumnWidth(1, 100)
        self.tableTypesResearch.setColumnWidth(2, 150)
        self.tableTypesResearch.setColumnWidth(3, 130)

        btnSave = QtWidgets.QPushButton(widget)
        btnSave.setText('Сохранить')
        btnSave.setGeometry(QtCore.QRect(350, 400, 100, 30))
        btnSave.clicked.connect(lambda: self.save())

        self.mess = QtWidgets.QLabel(widget)
        self.mess.setGeometry(QtCore.QRect(300, 450, 200, 40))
        self.mess.setStyleSheet('color: rgb(200, 0, 0)')

    def searchClients(self):
        self.get_connect()
        self.comboBox.clear()
        nameClient = self.line_client.text()
        if nameClient != '':
            query = f'''SELECT id, CONCAT_WS(' ', number, client)
            FROM contract
            WHERE client LIKE '%{nameClient}%'
            OR number LIKE '%{nameClient}%';'''
            self.answ_client = self.db.query(query)

            list_client = []
            for i in self.answ_client:
                list_client.append(i[1])
            self.comboBox.addItems(list_client)
        else:
            self.comboBox.clear()

    def save(self):
        number = self.lineNumber.text().strip()
        date = list(map(int, self.lineDate.text().split('.')))
        date = datetime.date(date[2], date[1], date[0])
        contract = self.comboBox.currentIndex()
        samples_rp = self.lineSampleRP.text().strip()
        target = self.lineTarget.text().strip()
        if contract == -1:
            self.mess.setText('Выберете Договор')
        elif number == '':
            self.mess.setText('Введите номер')
        elif number.strip().isdigit() is False:
            self.mess.setText('Некорректный номер')
        elif date == datetime.date(2000, 1, 1):
            self.mess.setText('Введите дату')
        elif self.check(number, date, contract):
            self.mess.setText('Такая Заявка уже существует')
        elif samples_rp == '':
            self.mess.setText('Введите объект исследования')
        elif target == '':
            self.mess.setText('Введите цель исследования')
        else:
            self.saveApplicatContract(
                number, date, contract, samples_rp, target)

    def check(self, number, date, contract):
        idC = self.answ_client[contract][0]
        query = f'''SELECT number, date, contract_id
        FROM applic_contract WHERE contract_id = {idC};'''
        answApplicContract = self.db.query(query)
        tup = (int(number), date, idC)
        return tup in answApplicContract

    def saveApplicatContract(self, number, date, contract, samples_rp, target):
        query = ('''INSERT INTO applic_contract
                    (number, date, contract_id, samples_rp, target, status)
                    VALUES (%s, %s, %s, %s, %s, %s);''')
        self.db.query_insert(query, (
                        int(number), date, self.answ_client[contract][0],
                        samples_rp, target, 1))
        text = 'Сохранено'
        idAC = self.db.query('''SELECT MAX(id) FROM applic_contract''')[0][0]
        res = []
        query = ('''INSERT INTO types_of_research (
                   type_research, count_sample,
                   deadline, price, applic_contract_id)
                   VALUES (%s, %s, %s, %s, %s)''')
        for i in range(15):
            tup = tuple()
            for j in range(4):
                a = self.tableTypesResearch.item(i, j).text().strip()
                if j == 3:
                    a = a.replace(' ', '').replace(',', '.')
                tup += (a,)
            if tup == ('', '', '', ''):
                continue
            else:
                tup += (idAC,)
                res.append(tup)

        if res == []:
            text += '\nВиды работ не внесены'
        else:
            for i in res:
                self.db.query_insert(query, i)
            price = float(self.db.query(f'''SELECT SUM(price)
            FROM types_of_research
            WHERE applic_contract_id = {idAC};''')[0][0])
            nds = (price * 20) / 120
            self.db.query_insert(f'''UPDATE applic_contract SET
            price = {price}, nds = {nds} WHERE id = {idAC}''')

        self.mess.setText(text)
        self.clearFields()

    def clearFields(self):
        self.line_client.setText('')
        self.lineNumber.setText('')
        self.lineDate.setDate(QtCore.QDate(2000, 1, 1))
        self.comboBox.clear()
        self.lineSampleRP.setText('')
        self.lineTarget.setText('')
        for i in range(15):
            for j in range(4):
                item = QtWidgets.QTableWidgetItem()
                self.tableTypesResearch.setItem(i, j, item)
