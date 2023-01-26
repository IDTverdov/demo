# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
from select_sample import Ui_Select_sample
from select_user import Ui_Select_user
from get_start import Start_App
from connect.connect import DataBase


class Ui_Applic(object):
    answ_client = None
    my_list_samp = None
    ids_uhtm = None
    ids_samp = None
    ids_met = None
    id_applic = None
    fnBtnToApplic = None

    def __init__(self):
        super().__init__()

    def get_connect(self):
        self.db = DataBase()
        self.db.connect()

    def applic(self, widget, fnBtnToApplic, mw):
        self.fnBtnToApplic = fnBtnToApplic
        self.fnBtnToApplic(widget)
        # self.get_connect()

        # Заголовок
        applicatTitle = QtWidgets.QLabel(widget)
        applicatTitle.setGeometry(QtCore.QRect(295, 20, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        applicatTitle.setFont(font)
        applicatTitle.setText("Заявка")

        # Номер Договора
        contractLabel = QtWidgets.QLabel(widget)
        contractLabel.setGeometry(QtCore.QRect(140, 60, 120, 20))
        contractLabel.setText("Договор/Заказчик")
        self.line_contract = QtWidgets.QLineEdit(widget)
        self.line_contract.setGeometry(QtCore.QRect(240, 60, 160, 20))
        # self.line_contract.returnPressed.connect(lambda: self.searchContract())
        self.comboBoxContract = QtWidgets.QComboBox(widget)
        self.comboBoxContract.setGeometry(QtCore.QRect(410, 60, 200, 20))
        btnContract = QtWidgets.QPushButton(widget)
        btnContract.setGeometry(QtCore.QRect(280, 95, 60, 30))
        btnContract.setText('Выбрать')
        # btnContract.clicked.connect(lambda: self.searchAppContract(
        #     self.comboBoxContract.currentIndex()))
        appContrLabel = QtWidgets.QLabel(widget)
        appContrLabel.setText('Заявка по Договору')
        appContrLabel.setGeometry(QtCore.QRect(160, 100, 110, 20))
        self.comboBoxAppContract = QtWidgets.QComboBox(widget)
        self.comboBoxAppContract.setGeometry(QtCore.QRect(360, 100, 200, 20))

        # Виды работ
        self.tableWork = QtWidgets.QTableWidget(widget)
        self.tableWork.setGeometry(QtCore.QRect(150, 230, 400, 100))

        # Примечания
        self.label_info = QtWidgets.QLabel(widget)
        self.label_info.setGeometry(QtCore.QRect(238, 120, 150, 50))
        self.label_info.setText("            Примечания\n(до 1000 символов)")

        self.info = QtWidgets.QTextEdit(widget)
        self.info.setGeometry(QtCore.QRect(345, 130, 215, 50))

        # Кнопка Сохранить
        self.btn_save = QtWidgets.QPushButton(widget)
        self.btn_save.setGeometry(QtCore.QRect(305, 360, 100, 30))
        self.btn_save.setText("Сохранить")
        self.btn_save.clicked.connect(lambda: self.get_start())

        # Кнопка выбора образцов
        self.btn_select_smp = QtWidgets.QPushButton(widget)
        self.btn_select_smp.setGeometry(QtCore.QRect(195, 190, 140, 30))
        self.btn_select_smp.clicked.connect(lambda: self.select_sample(mw))
        self.btn_select_smp.setText("Выбрать образцы")

        # Кнопка выбора сотрудников
        self.btn_select_usr = QtWidgets.QPushButton(widget)
        self.btn_select_usr.setGeometry(QtCore.QRect(345, 190, 140, 30))
        self.btn_select_usr.clicked.connect(lambda: self.select_user(mw))
        self.btn_select_usr.setText("Выбрать испытания")

        # Текст сообщения
        self.text_messege = QtWidgets.QLabel(widget)
        self.text_messege.setGeometry(QtCore.QRect(300, 370, 280, 90))
        self.text_messege.setStyleSheet('color: rgb(200, 0, 0)')

        QtCore.QMetaObject.connectSlotsByName(widget)

    def searchContract(self):
        self.get_connect()
        self.comboBoxContract.clear()
        nameContract = self.line_contract.text()
        if nameContract != '':
            query = f'''SELECT id, CONCAT_WS(' ', number, client)
            FROM contract
            WHERE client LIKE '%{nameContract}%'
            OR number LIKE '%{nameContract}%';'''
            self.answ_client = self.db.query(query)

            list_contract = []
            for i in self.answ_client:
                list_contract.append(i[1])
            self.comboBoxContract.addItems(list_contract)
        else:
            self.comboBoxContract.clear()

    def searchAppContract(self, index_contract):
        self.get_connect()
        self.comboBoxAppContract.clear()
        if index_contract != -1:
            query = f'''SELECT id, CONCAT_WS(' от ', number, DATE_FORMAT(date,'%d.%m.%Y'))
            FROM applic_contract
            WHERE contract_id = {self.answ_client[index_contract][0]}
            AND status = 1;'''
            self.answ_AC = self.db.query(query)

            list_AC = []
            for i in self.answ_AC:
                list_AC.append(i[1])
            self.comboBoxAppContract.addItems(list_AC)
        else:
            self.comboBoxAppContract.clear()

    def select_sample(self, mw):
        '''Функция выбора образцов'''
        global Dialog
        self.ids_samp = []
        self.ids_met = []
        self.text_messege.setText('')
        Dialog = QtWidgets.QDialog(mw)
        uss = Ui_Select_sample()
        uss.select_sample(Dialog)
        uss.setHandler(self.list_cb_sample)
        Dialog.show()

    def select_user(self, mw):
        '''Функция выбора сотрудников'''
        global Dialog
        Dialog = QtWidgets.QDialog(mw)
        usu = Ui_Select_user()
        usu.setView(self.ids_met)
        usu.select_user(Dialog)
        usu.setHandler(self.list_cb_usr)
        Dialog.show()

    def list_cb_sample(self, check):
        '''Считывание с формы образцов'''
        self.get_connect()
        self.my_list_samp = check

        for i in self.my_list_samp:
            self.ids_samp.append(i[0])
            self.ids_met.append(i[1])
        self.ids_met = sorted(list(set(self.ids_met)))
        idsSamp = sorted(list(set(self.ids_samp)))
        self.text_messege.setText(f'Выбрано образцов: {len(idsSamp)}')
        self.tableWork.setColumnCount(1)
        self.tableWork.setColumnWidth(0, 350)
        self.tableWork.setHorizontalHeaderLabels(
            ['Виды работ (до 500 символов)'])
        idsMetStr = [str(i) for i in self.ids_met]
        self.logs = self.db.query(
            f'''SELECT log
            FROM method WHERE id IN ({', '.join(idsMetStr)});''')
        self.logs = [i[0] for i in self.logs]
        self.tableWork.setRowCount(len(self.logs))
        self.tableWork.setVerticalHeaderLabels(self.logs)
        for i in range(len(self.logs)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWork.setItem(i, 0, item)
            item = self.tableWork.item(i, 0)
            item.setText('')
        Dialog.close()

        # Считывание с формы сотрудников
    def list_cb_usr(self, check):
        self.ids_uhtm = check
        if self.ids_uhtm is not None:
            self.text_messege.setText(
                f'Выбрано анализов: {len(self.ids_uhtm)}')
        Dialog.close()

        # Очистка полей
    def clear_filds(self):
        self.line_contract.setText('')
        self.comboBoxContract.clear()
        self.comboBoxAppContract.clear()
        self.info.setText('')
        self.ids_samp = None
        self.ids_met = None
        self.tableWork.setRowCount(0)

        # Функция Старт
    def get_start(self):
        if self.comboBoxContract.currentIndex() == -1:
            self.text_messege.setText('Не выбран Договор')
        elif self.comboBoxAppContract.currentIndex() == -1:
            self.text_messege.setText('Не выбрана Заявка по Договору')
        elif self.ids_samp == []:
            self.text_messege.setText("Не выбраны образцы")
        elif self.ids_uhtm == [] or self.ids_uhtm is None:
            self.text_messege.setText("Не выбраны испытания")

        elif (self.db.query(
            f"""SELECT date_end
            FROM contract
            WHERE id = {
            self.answ_client[self.comboBoxContract.currentIndex()][0]
            }""")[0][0]
             ) < datetime.date(datetime.now()):
            self.text_messege.setText("Истёк срок действия Договора")
        else:
            idContract = self.answ_client[
                self.comboBoxContract.currentIndex()][0]
            idAppContract = self.answ_AC[
                self.comboBoxAppContract.currentIndex()][0]
            info = self.info.toPlainText()
            typesWork = []
            for i in range(self.tableWork.rowCount()):
                typesWork.append(self.tableWork.item(i, 0).text())

            start = Start_App()
            start.join_method(self.my_list_samp)
            self.id_applic = start.insert_applic(
                self.logs, idAppContract, idContract, info)
            name = self.db.query(f'''SELECT name
            FROM applicat WHERE id = {self.id_applic}''')
            self.text_messege.setText(
                f'             Сохранено \n Заявка №{name[0][0]}')
            self.db.insert_log(f'Внесена Заявка №{name[0][0]}')
            start.join_sample(self.ids_samp, idAppContract, self.id_applic)
            start.join_user(self.id_applic, self.ids_uhtm)
            start.join_report(
                self.id_applic, self.logs, typesWork, self.ids_met)
            start.write_aplic(self.id_applic, self.ids_uhtm)
            self.clear_filds()
