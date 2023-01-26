# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase


class Ui_Usrs:
    db = None
    cb = None
    answ_usr = None
    widget = None
    subWidget = None
    answ_usr_for_table = None

    def get_connect(self):
        self.db = DataBase()
        self.answ_usrs = self.db.query('''SELECT name FROM user
        WHERE id IN (SELECT user_id FROM user_work);''')
        self.answ_usrs = [
            self.answ_usrs[i][0] for i in range(len(self.answ_usrs))]
        self.answ_usrs = ['Выбрать сотрудника:'] + self.answ_usrs

        self.answ_usr_for_table = self.db.query('''SELECT name, job, email
        FROM user WHERE id IN (SELECT user_id FROM user_work);''')
        self.answ_usr_for_table.sort(key=lambda i: i[0])

    def show(self, widget, setupWidget, fnBtnToUsr, mw):
        self.mw = mw
        self.widget = widget
        self.setupWidget = setupWidget
        self.fnBtnToUsr = fnBtnToUsr

        # self.get_connect()
        title_usrs = QtWidgets.QLabel(self.widget)
        title_usrs.setGeometry(QtCore.QRect(280, 40, 420, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title_usrs.setFont(font)
        title_usrs.setText("Сотрудники")

        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 100, 600, 300))
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        head_list = ['Фамилия Имя Отчество', 'Должность', 'email']
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(head_list)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        # n = len(self.answ_usr_for_table)
        # self.tableWidget.setRowCount(n)
        # for i in range(n):
        #     for j in range(3):
        #         item = QtWidgets.QTableWidgetItem()
        #         self.tableWidget.setItem(i, j, item)
        #         item = self.tableWidget.item(i, j)
        #         item.setText(str(self.answ_usr_for_table[i][j]))

        btn_append = QtWidgets.QPushButton(self.widget)
        btn_append.setGeometry(QtCore.QRect(85, 420, 150, 30))
        btn_append.setText('Добавить сотрудника')
        btn_append.clicked.connect(lambda: self.usrAppend(self.fnBtnToUsr))

        btn_change = QtWidgets.QPushButton(self.widget)
        btn_change.setGeometry(QtCore.QRect(245, 420, 150, 30))
        btn_change.setText('Внести изменения')
        btn_change.clicked.connect(lambda: self.usrChange(self.fnBtnToUsr))

        btn_delete = QtWidgets.QPushButton(self.widget)
        btn_delete.setGeometry(QtCore.QRect(405, 420, 150, 30))
        btn_delete.setText('Удалить сотрудника')
        btn_delete.clicked.connect(lambda: self.usrDelete(self.fnBtnToUsr))

    def usrAppend(self, fnBtnUsr):
        fnBtnUsr = fnBtnUsr
        self.widget = self.setupWidget()
        fnBtnUsr(self.widget)
        self.winAppend(self.widget)
        self.widget.show()

    def usrChange(self, fnBtnUsr):
        fnBtnUsr = fnBtnUsr
        self.widget = self.setupWidget()
        fnBtnUsr(self.widget)
        self.winChange(self.widget)
        self.widget.show()

    def usrDelete(self, fnBtnUsr):
        fnBtnUsr = fnBtnUsr
        self.widget = self.setupWidget()
        fnBtnUsr(self.widget)
        self.winDelete(self.widget)
        self.widget.show()

    def winAppend(self, widget):
        title = QtWidgets.QLabel(widget)
        title.setText('Добавить сотрудника')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setGeometry(QtCore.QRect(255, 40, 250, 30))

        label_family = QtWidgets.QLabel(widget)
        label_family.setText('Фамилия')
        label_family.setGeometry(QtCore.QRect(90, 100, 50, 20))
        self.family = QtWidgets.QLineEdit(widget)
        self.family.setGeometry(QtCore.QRect(160, 100, 150, 20))

        label_name = QtWidgets.QLabel(widget)
        label_name.setText('Имя')
        label_name.setGeometry(QtCore.QRect(90, 130, 50, 20))
        self.name = QtWidgets.QLineEdit(widget)
        self.name.setGeometry(QtCore.QRect(160, 130, 150, 20))

        label_sname = QtWidgets.QLabel(widget)
        label_sname.setText('Отчество')
        label_sname.setGeometry(QtCore.QRect(90, 160, 50, 20))
        self.sname = QtWidgets.QLineEdit(widget)
        self.sname.setGeometry(QtCore.QRect(160, 160, 150, 20))

        label_job = QtWidgets.QLabel(widget)
        label_job.setText('Должность')
        label_job.setGeometry(QtCore.QRect(325, 100, 60, 20))
        self.job = QtWidgets.QLineEdit(widget)
        self.job.setGeometry(QtCore.QRect(390, 100, 150, 20))

        label_email = QtWidgets.QLabel(widget)
        label_email.setText('email')
        label_email.setGeometry(QtCore.QRect(355, 130, 60, 20))
        self.email = QtWidgets.QLineEdit(widget)
        self.email.setGeometry(QtCore.QRect(390, 130, 150, 20))

        btn_method = QtWidgets.QPushButton(widget)
        btn_method.setText('Выбрать метод')
        btn_method.setGeometry(QtCore.QRect(390, 160, 150, 30))
        btn_method.clicked.connect(self.selectMethod)

        btn_save = QtWidgets.QPushButton(widget)
        btn_save.setText('Сохранить')
        btn_save.setGeometry(QtCore.QRect(270, 200, 100, 30))
        btn_save.clicked.connect(lambda: self.get_save())

        self.mess_txt = QtWidgets.QLabel(widget)
        self.mess_txt.setGeometry(QtCore.QRect(180, 250, 160, 100))

    def winChange(self, widget):
        title = QtWidgets.QLabel(widget)
        title.setText('Внести изменения')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setGeometry(QtCore.QRect(240, 40, 200, 30))

        self.comboBox = QtWidgets.QComboBox(widget)
        # self.comboBox.addItems(self.answ_usrs)
        self.comboBox.setGeometry(QtCore.QRect(215, 100, 250, 30))

        label_family = QtWidgets.QLabel(widget)
        label_family.setText('Фамилия')
        label_family.setGeometry(QtCore.QRect(90, 150, 50, 20))
        self.family = QtWidgets.QLineEdit(widget)
        self.family.setGeometry(QtCore.QRect(160, 150, 150, 20))

        label_name = QtWidgets.QLabel(widget)
        label_name.setText('Имя')
        label_name.setGeometry(QtCore.QRect(90, 180, 50, 20))
        self.name = QtWidgets.QLineEdit(widget)
        self.name.setGeometry(QtCore.QRect(160, 180, 150, 20))

        label_sname = QtWidgets.QLabel(widget)
        label_sname.setText('Отчество')
        label_sname.setGeometry(QtCore.QRect(90, 210, 50, 20))
        self.sname = QtWidgets.QLineEdit(widget)
        self.sname.setGeometry(QtCore.QRect(160, 210, 150, 20))

        label_job = QtWidgets.QLabel(widget)
        label_job.setText('Должность')
        label_job.setGeometry(QtCore.QRect(325, 150, 60, 20))
        self.job = QtWidgets.QLineEdit(widget)
        self.job.setGeometry(QtCore.QRect(390, 150, 150, 20))

        label_email = QtWidgets.QLabel(widget)
        label_email.setText('email')
        label_email.setGeometry(QtCore.QRect(355, 180, 60, 20))
        self.email = QtWidgets.QLineEdit(widget)
        self.email.setGeometry(QtCore.QRect(390, 180, 150, 20))

        btn_method = QtWidgets.QPushButton(widget)
        btn_method.setText('Выбрать метод')
        btn_method.setGeometry(QtCore.QRect(390, 210, 150, 30))
        btn_method.clicked.connect(self.selectMethod)

        btn_save = QtWidgets.QPushButton(widget)
        btn_save.setText('Изменить')
        btn_save.setGeometry(QtCore.QRect(270, 250, 100, 30))
        btn_save.clicked.connect(lambda: self.get_change())

        self.mess_txt = QtWidgets.QLabel(widget)
        self.mess_txt.setGeometry(QtCore.QRect(200, 300, 100, 30))

    def winDelete(self, widget):
        title = QtWidgets.QLabel(widget)
        title.setText('Удалить сотрудника')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setGeometry(QtCore.QRect(240, 40, 220, 30))

        self.comboBox = QtWidgets.QComboBox(widget)
        # self.comboBox.addItems(self.answ_usrs)
        self.comboBox.setGeometry(QtCore.QRect(125, 100, 250, 30))

        btn_delete = QtWidgets.QPushButton(widget)
        btn_delete.setText('Удалить')
        btn_delete.setGeometry(QtCore.QRect(200, 150, 100, 30))
        btn_delete.clicked.connect(lambda: self.get_delete())

        self.mess_txt = QtWidgets.QLabel(widget)
        self.mess_txt.setGeometry(QtCore.QRect(180, 200, 160, 100))

    def get_save(self):
        family = self.family.text().strip()
        name = self.name.text().strip()
        sname = self.sname.text().strip()
        job = self.job.text().strip()
        email = self.email.text().strip()

        con = 0
        for i in email:
            if (1040 <= ord(i) <= 1105) or (
                   ord(i) == 1025) or (ord(i) == 1105):
                con = 1

        if family == '':
            self.mess_txt.setText('Введите фамилию')
        elif name == '':
            self.mess_txt.setText('Введите имя')
        elif job == '':
            self.mess_txt.setText('Введите должность')
        elif email == '':
            self.mess_txt.setText('Введите email')
        elif '@' not in email or con == 1:
            self.mess_txt.setText('Некорректный email')
        elif self.cb is None or self.cb == []:
            self.mess_txt.setText('Не выбран метод')

        else:
            self.get_to_db(family, name, sname, job, email)
            self.mess_txt.setText(f'''           Сотрудник \n\n {
                family} {name} {sname} \n\n             сохранён''')
            self.clear_fields()
            self.get_update()

    def get_change(self):
        name_cb = self.comboBox.currentText()
        family = self.family.text().strip()
        name = self.name.text().strip()
        sname = self.sname.text().strip()
        job = self.job.text().strip()
        email = self.email.text().strip()

        if name_cb == 'Выбрать сотрудника:':
            self.mess_txt.setText('Не выбрано')

        else:
            usr_id = self.db.query(f'''SELECT id FROM user
            WHERE name = '{name_cb}' ''')[0][0]

            if family != '':
                fio = self.db.query(f'''SELECT name FROM user
                WHERE id = {usr_id}''')[0][0].split()

                fio[0] = family
                fio = ' '.join(fio)
                self.db.query_insert(f'''UPDATE user SET name = '{fio}'
                WHERE id = {usr_id}''')
                queryLog = f'Изменена фамилия сотрудника {fio}'
                self.db.insert_log(queryLog)
                self.mess_txt.setText('Изменения внесены')
                self.clear_fields()
                self.clear_comboBox()
                self.get_update()

            if name != '':
                fio = self.db.query(f'''SELECT name FROM user
                WHERE id = {usr_id}''')[0][0].split()
                fio[1] = name
                fio = ' '.join(fio)
                self.db.query_insert(f'''UPDATE user SET name = '{fio}'
                WHERE id = {usr_id}''')
                queryLog = f'Изменено имя сотрудника {fio}'
                self.db.insert_log(queryLog)
                self.mess_txt.setText('Изменения внесены')
                self.clear_fields()
                self.clear_comboBox()
                self.get_update()

            if sname != '':
                fio = self.db.query(f'''SELECT name FROM user
                WHERE id = {usr_id}''')[0][0].split()
                fio[2] = sname
                fio = ' '.join(fio)
                self.db.query_insert(f'''UPDATE user SET name = '{fio}'
                WHERE id ={usr_id}''')
                queryLog = f'Изменено отчество сотрудника {fio}'
                self.db.insert_log(queryLog)
                self.mess_txt.setText('Изменения внесены')
                self.clear_fields()
                self.clear_comboBox()
                self.get_update()

            if job != '':
                self.db.query_insert(f'''UPDATE user SET job = '{job}'
                WHERE id = {usr_id}''')
                fio = self.db.query(f'''SELECT name FROM user
                WHERE id = {usr_id}''')[0][0]
                queryLog = f'Изменена должность сотрудника {fio}'
                self.db.insert_log(queryLog)
                self.mess_txt.setText('Изменения внесены')
                self.clear_fields()
                self.clear_comboBox()
                self.get_update()

            if email != '':
                con = 0
                for i in email:
                    if (1040 <= ord(i) <= 1105) or (
                           ord(i) == 1025) or (ord(i) == 1105):
                        con = 1
                if '@' not in email or con == 1:
                    self.mess_txt.setText('Некорректный email')
                else:
                    self.db.query_insert(f'''UPDATE user SET email = '{email}'
                    WHERE id = {usr_id}''')
                    fio = self.db.query(f'''SELECT name FROM user
                    WHERE id = {usr_id}''')[0][0]
                    queryLog = f'Изменён email сотрудника {fio}'
                    self.db.insert_log(queryLog)
                    self.mess_txt.setText('Изменения внесены')
                    self.clear_fields()
                    self.clear_comboBox()
                    self.get_update()

            if self.cb != []:
                if type(self.cb) == list:
                    self.db.query_insert(f'''DELETE FROM user_has_type_method
                    WHERE user_id = {usr_id}''')
                    fio = self.db.query(f'''SELECT name FROM user
                    WHERE id = {usr_id}''')[0][0]
                    for i in self.cb:
                        query = f'''INSERT INTO user_has_type_method
                        (user_id, type_method_id) VALUES ({usr_id}, {i+1});'''
                        self.db.query_insert(query)

                    queryLog = 'Изменён метод сотрудника ' + fio
                    self.db.insert_log(queryLog)
                    self.mess_txt.setText('Изменения внесены')
                    self.clear_comboBox()
                    self.get_update()

    def get_delete(self):
        name = self.comboBox.currentText()
        if name == 'Выбрать сотрудника:':
            self.mess_txt.setText('Не выбрано')
        else:
            usr_id = self.db.query(f'''SELECT id FROM user
            WHERE name = '{name}' ''')[0][0]
            self.db.query_insert(f'''DELETE FROM user_work
            WHERE user_id = {usr_id}''')
            self.db.query_insert(f'''DELETE FROM user_has_type_method
            WHERE user_id = {usr_id}''')
            queryLog = f'Удалён сотрудник {name}'
            self.db.insert_log(queryLog)
            self.mess_txt.setText(f'''           Сотрудник \n\n{
                name}\n\n             удалён''')
            self.clear_comboBox()

    def clear_fields(self):
        self.family.setText('')
        self.name.setText('')
        self.sname.setText('')
        self.job.setText('')
        self.email.setText('')

    def clear_comboBox(self):
        self.comboBox.clear()
        self.get_update()
        self.comboBox.addItems(self.answ_usrs)

    def get_to_db(self, family, name, sname, job, email):
        fio = family + ' ' + name + ' ' + sname
        fio = fio.strip()
        query = '''INSERT INTO user (name, job, email) VALUES (%s, %s, %s) '''
        val = (fio, job, email)
        self.db.query_insert(query, val)
        queryLog = 'Добавлен сотрудник ' + fio
        self.db.insert_log(queryLog)
        usr_id = self.db.query('''SELECT MAX(id) FROM user''')[0][0]
        self.db.query_insert(f'''INSERT INTO user_work (user_id)
        VALUES ({usr_id});''')

        for i in self.cb:
            query = f'''INSERT INTO user_has_type_method
            (user_id, type_method_id) VALUES ({usr_id}, {i+1});'''
            self.db.query_insert(query)

    def get_update(self):
        self.get_connect()
        lenght = len(self.answ_usr_for_table)
        self.tableWidget.setRowCount(lenght)
        for i in range(lenght):
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)
                item.setText(str(self.answ_usr_for_table[i][j]))

    def selectMethod(self):
        global Dialog
        Dialog = QtWidgets.QDialog(self.mw)
        self.windSelectMethod(Dialog)
        self.setHandler(self.selectedCB)
        Dialog.show()

    def windSelectMethod(self, Dialog):
        Dialog.resize(600, 400)
        Dialog.setWindowTitle('Выберете метод')
        self.get_connect()

        self.answMethod = self.db.query('''SELECT id, (SELECT name FROM method
        WHERE id = type_method.method_id), name FROM type_method''')
        a = len(self.answMethod)
        headList = ['Метод', 'Анализ', ' ']
        b = len(headList)

        title = QtWidgets.QLabel(Dialog)
        title.setText('Выберете метод')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)
        title.setGeometry(QtCore.QRect(200, 20, 200, 30))

        self.table = QtWidgets.QTableWidget(Dialog)
        self.table.setGeometry(QtCore.QRect(20, 70, 560, 250))
        self.table.setColumnCount(b)
        self.table.setRowCount(a)
        self.table.setHorizontalHeaderLabels(headList)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)

        for i in range(a):
            for j in range(b):
                item = QtWidgets.QTableWidgetItem()
                if 0 <= j <= 1:
                    self.table.setItem(i, j, item)
                    item = self.table.item(i, j)
                    item.setText(str(self.answMethod[i][j+1]))
                else:
                    f = QtWidgets.QWidget()
                    checkbox = QtWidgets.QCheckBox()
                    layO = QtWidgets.QHBoxLayout(f)
                    layO.setAlignment(QtCore.Qt.AlignCenter)
                    layO.addWidget(checkbox)
                    layO.setContentsMargins(0, 0, 0, 0)
                    self.table.setCellWidget(i, j, f)

        btn = QtWidgets.QPushButton(Dialog)
        btn.setGeometry(QtCore.QRect(250, 340, 100, 30))
        btn.setText('Выбрать')
        btn.clicked.connect(lambda: self.cb(self.fnSelectMethod()))

    def setHandler(self, cb=None):
        self.cb = cb

    def selectedCB(self, check=None):
        if self.cb is not None:
            self.cb = check
            self.mess_txt.setText('Метод выбран')
            Dialog.close()
        else:
            Dialog.close()

    def fnSelectMethod(self):
        checked = []
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 2).findChild(
                     type(QtWidgets.QCheckBox())).isChecked():
                checked.append(i)
        return checked
