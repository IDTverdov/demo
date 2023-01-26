# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from connect.connect import DataBase
from applic_viewer import Applic_Viewer
from contract_viewer import ConactViewer
from applic_knitu_viewer import Applic_KNITU


class Ui_Source(object):
    db = None
    answ_applic = None
    answ_contr = None
    answ_samp = None
    setupCentralWidget = None
    btnHome = None
    countRows = None

    def get_connect(self):
        '''Соединение с БД, объявление переменных с ответами таблицы
        Договоров, Заявок, образцов и Заявок по Договорам'''
        self.db = DataBase()
        self.answ_contr = self.db.query(
            '''SELECT id, DATE_FORMAT(date_start, '%d.%m.%Y'), number, client,
            phone, adress, (SELECT COUNT(id) FROM applic_contract
            WHERE contract_id = contract.id),
            DATE_FORMAT(date_end, '%d.%m.%Y') FROM contract;''')
        self.answ_applic = self.db.query(
            '''SELECT id, DATE_FORMAT(date, '%d.%m.%Y'), name,
            (SELECT CONCAT_WS(', ', contract.number, contract.client)
            FROM contract WHERE id = applicat.contract_id),
            (SELECT number FROM applic_contract
            WHERE id = applicat.applic_contract_id),
            info, (SELECT COUNT(id) FROM sample
            WHERE applicat_id = applicat.id),
            IF(status = 0, 'Аннулировано',
            IF(status = 1, 'В работе', 'Выполнено')) FROM applicat;''')
        self.answ_samp = self.db.query(
            '''SELECT sample.id, DATE_FORMAT(sample.date, '%d.%m.%Y'),
            sample.number, sample.name, applicat.name,
            sample.type, CONCAT_WS(', ', contract.number, contract.client),
            GROUP_CONCAT(DISTINCT type_method.name ORDER BY 1 SEPARATOR ', ')
            FROM sample
            JOIN applicat ON applicat.id = sample.applicat_id
            JOIN applicat_has_uhtm ON
                applicat_has_uhtm.applicat_id = applicat.id
            JOIN user_has_type_method ON
            applicat_has_uhtm.user_has_type_method_id = user_has_type_method.id
            JOIN type_method
                ON user_has_type_method.type_method_id = type_method.id
            JOIN contract ON applicat.contract_id = contract.id
            GROUP BY 1 ORDER BY 1;''')
        self.answ_applic_kn = self.db.query(
            '''SELECT applic_contract.id, DATE_FORMAT(date, '%d.%m.%Y'),
            applic_contract.number, contract.number,
            contract.client, (SELECT COUNT(id) FROM applicat
            WHERE applic_contract_id = applic_contract.id), price,
            IF(status = 0, 'Аннулировано',
            IF(status = 1, 'В работе', 'Выполнено'))
            FROM applic_contract
            JOIN contract ON applic_contract.contract_id = contract.id;''')

    def source(self, setupCentralWidget, btnHome):
        '''Отрисовка окна обозревателя'''
        self.setupCentralWidget = setupCentralWidget
        self.btnHome = btnHome
        self.centralWidget = QtWidgets.QWidget()
        self.setupCentralWidget(self.centralWidget)
        self.btnHome(self.centralWidget)

        # self.get_connect()

        searchLabel = QtWidgets.QLabel(self.centralWidget)
        searchLabel.setGeometry(QtCore.QRect(80, 80, 50, 20))
        searchLabel.setText("Запрос: ")

        self.countRows = QtWidgets.QLabel(self.centralWidget)
        self.countRows.setGeometry(QtCore.QRect(80, 105, 120, 20))

        # Кнопка запуска поиска
        btnSearch = QtWidgets.QPushButton(self.centralWidget)
        btnSearch.setGeometry(QtCore.QRect(910, 75, 80, 30))
        btnSearch.setAutoDefault(True)
        btnSearch.setText("Поиск")
        btnSearch.clicked.connect(lambda: self.search())

        self.line_sourse = QtWidgets.QLineEdit(self.centralWidget)
        self.line_sourse.setGeometry(QtCore.QRect(120, 80, 780, 20))
        self.line_sourse.returnPressed.connect(btnSearch.click)

        # Отрисовка поля для таблиц и вызов первой
        self.setupSubWidgetSource()
        self.contractWidget()

        # Кнопки для переключения
        # Кнопка Договор
        btn_contracs = QtWidgets.QPushButton(self.centralWidget)
        btn_contracs.setGeometry(QtCore.QRect(285, 30, 110, 40))
        btn_contracs.setText("Договоры")
        btn_contracs.clicked.connect(self.contractWidget)

        # Кнопка Заявка по Договору
        btn_applicat_kn = QtWidgets.QPushButton(self.centralWidget)
        btn_applicat_kn.setGeometry(QtCore.QRect(415, 30, 110, 40))
        btn_applicat_kn.setText("Заявки \nпо Договору")
        btn_applicat_kn.clicked.connect(self.applicatKNITUWidget)

        # Кнопка Заявка
        btn_applicat = QtWidgets.QPushButton(self.centralWidget)
        btn_applicat.setGeometry(QtCore.QRect(545, 30, 110, 40))
        btn_applicat.setText("Заявки")
        btn_applicat.clicked.connect(self.applicatWidget)

        # Кнопка Образцы
        btn_samples = QtWidgets.QPushButton(self.centralWidget)
        btn_samples.setGeometry(QtCore.QRect(675, 30, 110, 40))
        btn_samples.setText("Образцы")
        btn_samples.clicked.connect(self.sampleWidget)

        QtCore.QMetaObject.connectSlotsByName(self.centralWidget)

    def setupSubWidgetSource(self):
        '''Отрнисовка миниокна, где будут таблицы'''
        self.subWidgetSource = QtWidgets.QWidget(self.centralWidget)
        self.subWidgetSource.setGeometry(QtCore.QRect(20, 130, 1030, 600))

    def contractWidget(self):
        '''Отрисовка таблицы Договоров'''
        self.setupSubWidgetSource()

        # a = len(self.answ_contr)
        a = 0
        headList = ['Дата заключния \nДоговора', 'Номер \nДоговора',
                    'Наименование \nЗаказчика', 'Контактный \nтелефон',
                    'Адрес', 'Количество \nЗаявок \n по Договору',
                    'Дата окончания \nДоговора']
        b = len(headList)

        self.drawTable(self.subWidgetSource, headList, self.answ_contr, a, b)
        self.table.setColumnWidth(1, 70)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(4, 245)
        self.table.cellDoubleClicked.connect(
            lambda: self.contract_view(self.table.currentRow()))
        self.subWidgetSource.show()

    def contract_view(self, row):
        '''Окно обзора Договора'''
        self.centralWidget = QtWidgets.QWidget()
        self.setupCentralWidget(self.centralWidget)
        cw = ConactViewer()
        id = self.answ_contr[row][0]
        cw.viewer(self.centralWidget, self.setupCentralWidget,
                  self.btnHome, self.btnBackContract, id)

    def applic_contract_view(self, row):
        '''Окно обзора Заявки по Договору'''
        self.centralWidget = QtWidgets.QWidget()
        self.setupCentralWidget(self.centralWidget)
        acw = Applic_KNITU()
        id = self.answ_applic_kn[row][0]
        acw.viewer(self.centralWidget, self.btnHome, self.setupCentralWidget,
                   self.btnBackApplicContract, id)

    def applicViewer(self, row, answ, btnBack):
        '''Окно обзора Заявки'''
        self.centralWidget = QtWidgets.QWidget()
        self.setupCentralWidget(self.centralWidget)
        aw = Applic_Viewer()
        idCurrentApplic = answ[row][0]
        aw.viewer(
            self.centralWidget, self.setupCentralWidget, self.btnHome,
            btnBack, idCurrentApplic)

    def applicatKNITUWidget(self):
        '''Отрисовка таблицы Заявок по Договору'''
        self.subWidgetSource.hide()
        self.setupSubWidgetSource()

        # a = len(self.answ_applic_kn)
        a = 0
        headList = ['Дата Заявки \nпо Договору', 'Номер Заявки',
                    'к Договору №', 'Заказчик', 'Количество \nЗаявок',
                    'Цена с НДС', 'Статус']
        b = len(headList)

        self.drawTable(
            self.subWidgetSource, headList, [], a, b)
        self.table.cellDoubleClicked.connect(
            lambda: self.applic_contract_view(self.table.currentRow()))
        self.table.setColumnWidth(3, 250)
        self.subWidgetSource.show()

    def applicatWidget(self):
        '''Отрисовка таблицы Заявок'''
        self.subWidgetSource.hide()
        self.setupSubWidgetSource()
        # a = len(self.answ_applic)
        a = 0
        headList = ['Дата', 'Номер Заявки', 'Номер Договора',
                    'Номер \nЗаявки по \nДоговору', 'Примечания',
                    'Количество \nобразцов', 'Статус']
        b = len(headList)

        self.drawTable(self.subWidgetSource, headList, [], a, b)
        self.table.setColumnWidth(3, 230)
        self.table.cellDoubleClicked.connect(
            lambda: self.applicViewer(self.table.currentRow(),
                                      self.answ_applic, self.btnBackAplicat))
        self.subWidgetSource.show()

    def sampleWidget(self):
        '''Отрисовка таблицы Образцов'''
        self.subWidgetSource.hide()
        self.setupSubWidgetSource()
        # a = len(self.answ_samp)
        a = 0
        headList = ['Дата приёма', 'Лабораторный \nномер',
                    'Наименование образца \nЗаказчика',
                    'Номер Заявки/\n Акт приёма проб',
                    'Описание образца', 'Номер Договора\n  Заказчик',
                    'Метод анализа']
        b = len(headList)
        self.drawTable(self.subWidgetSource, headList, [], a, b)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 160)
        self.table.setColumnWidth(5, 230)
        self.subWidgetSource.show()

    def search(self, value=None):
        '''Функция поиска по таблице'''
        if value is None:
            value = self.line_sourse.text()
            value = str(value)

        result = self.table.findItems(value, QtCore.Qt.MatchContains)
        rows = []
        for item in result:
            row = self.table.row(item)
            rows.append(row)
        for i in range(self.table.rowCount()):
            self.table.hideRow(i)
        rows = sorted(set(rows))
        for row in rows:
            self.table.showRow(row)
        self.countRows.setText(f'Количество строк: {len(rows)}')

    def drawTable(self, subWidgetSource, headList, answ, a=0, b=0):
        '''Отрисовка основной таблицы'''
        self.table = QtWidgets.QTableWidget(subWidgetSource)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setGeometry(QtCore.QRect(10, 10, 1010, 580))
        self.table.setRowCount(a)
        self.table.setColumnCount(b)
        self.table.setSortingEnabled(True)
        self.table.setHorizontalHeaderLabels(headList)
        self.table.scrollToBottom()
        for i in range(a):
            for j in range(b):
                item = QtWidgets.QTableWidgetItem()
                self.table.setItem(i, j, item)
                item = self.table.item(i, j)
                item.setText(f'{(answ[i][j+1])}')

        self.countRows.setText(f'Количество строк: {a}')

    def btnBackAplicat(self, widget):
        '''Кнопка "Назад" с переходом к окну просмотра,
        где в таблице будут Заявки'''
        btnBack = QtWidgets.QPushButton(widget)
        btnBack.setGeometry(QtCore.QRect(20, 70, 100, 30))
        btnBack.setText('Назад')
        btnBack.clicked.connect(lambda: (self.source(
            self.setupCentralWidget, self.btnHome), self.applicatWidget()))

    def btnBackContract(self, widget):
        '''Кнопка "Назад" с переходом к окну просмотра,
        где в таблице будут Договоры'''
        btnBack = QtWidgets.QPushButton(widget)
        btnBack.setGeometry(QtCore.QRect(20, 70, 100, 30))
        btnBack.setText('Назад')
        btnBack.clicked.connect(lambda: (self.source(
            self.setupCentralWidget, self.btnHome)))

    def btnBackApplicContract(self, widget):
        '''Кнопка "Назад" с переходом к окну просмотра,
        где в таблице будут Заявки по Договору'''
        btnBack = QtWidgets.QPushButton(widget)
        btnBack.setGeometry(QtCore.QRect(20, 70, 100, 30))
        btnBack.setText('Назад')
        btnBack.clicked.connect(lambda: (self.source(
            self.setupCentralWidget, self.btnHome),
            self.applicatKNITUWidget()))

    def btnBackSample(self, widget):
        '''Кнопка "Назад" с переходом к окну просмотра,
        где в таблице будут Образцы'''
        btnBack = QtWidgets.QPushButton(widget)
        btnBack.setGeometry(QtCore.QRect(20, 70, 100, 30))
        btnBack.setText('Назад')
        btnBack.clicked.connect(lambda: (self.source(
            self.setupCentralWidget, self.btnHome), self.sampleWidget()))
