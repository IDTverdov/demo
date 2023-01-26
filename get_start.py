# -*- coding: utf-8 -*-
from datetime import datetime

from connect.connect import DataBase
from connect.mail import Set_Mail
# import docx


class Start_App():
    db = None
    answ_appl = None
    num_applicat_kn = None
    date_appl_kn = None
    list_samp = None
    tuple_log = None
    last_id_app_kn = None
    id_con = None
    info = None
    type_work = None
    ids_samp = None
    ids_usr = None
    s_loc = None
    name = None

    def get_connect(self):
        self.db = DataBase()

    def readTxt(self):
        with open('parametres.txt', 'r', encoding='utf-8') as f:
            listParametres = f.readlines()
            self.dirApplic = listParametres[0]
            self.dirApplicUsr = listParametres[1]

        # Функия присвоения методов к пробом
    def join_method(self, list_samp):
        self.list_samp = list_samp
        self.get_connect()
        query = ('''INSERT INTO sample_has_method (sample_id, method_id)
                 VALUES (%s, %s);''')
        for i in self.list_samp:
            self.db.query_insert(query, i)

        # Функция сохранения Заявки и присваивания номера
    def insert_applic(self, logs, last_id_app_kn, id_con, info):
        self.last_id_app_kn = last_id_app_kn
        self.id_con = id_con
        self.info = info
        self.get_connect()
        answ_appl = self.db.query('''SELECT name FROM applicat;''')
        answ_samp = self.db.query('''SELECT date FROM sample;''')
        query = ('''INSERT INTO applicat
        (name, date, applic_contract_id, contract_id, info)
        VALUES (%s, current_date, %s, %s, %s);''')

        # Сравнение и присвоение номера (number, year)
        if len(answ_appl) != 0:
            last_name = answ_appl[-1][0].split('-')
            last_num = int(last_name[0])
            last_y = int(last_name[2])
            year = str(answ_samp[-1][0])
            year = int(year[2:4])
            if last_y == year:
                number = last_num+1
            else:
                number = 1
        else:
            number = 1
            year = str(datetime.now())[2:4]

        name = str(number) + '-' + ','.join(logs) + '-' + str(year)
        val = (name, self.last_id_app_kn, self.id_con, self.info)
        self.db.query_insert(query, val)

        last_id = self.db.query('''SELECT MAX(id) FROM applicat''')[0][0]
        return last_id

        # Функия присвоения Заявке проб
    def join_sample(self, ids_samp, id_app_kn, id_applic):
        self.ids_samp = ids_samp
        self.ids_samp = tuple(self.ids_samp)
        self.id_applic = id_applic
        self.id_app_kn = id_app_kn
        self.get_connect()

        self.ids_samp = [str(i) for i in self.ids_samp]

        query = f'''UPDATE sample SET applicat_id = {self.id_applic}
        WHERE id IN ({','.join(self.ids_samp)});'''
        self.db.query(query)
        query = f'''UPDATE sample SET applic_contract_id = {self.id_app_kn}
        WHERE id IN ({','.join(self.ids_samp)});'''
        self.db.query(query)

        # Функция добавления Исполнителей
    def join_user(self, id_applic, ids_uhtm):
        self.id_applic = id_applic
        self.ids_uhtm = ids_uhtm
        self.get_connect()

        query = ('''INSERT INTO applicat_has_uhtm
        (user_has_type_method_id, applicat_id) VALUES (%s,%s);''')

        for i in self.ids_uhtm:
            val = (i, self.id_applic)
            self.db.query_insert(query, val)

        # Подготовка протоколов
    def join_report(self, id_applic, logs, typesWork, ids_met):
        self.id_applic = id_applic

        last_name = self.db.query(f'''SELECT name FROM applicat
        WHERE id = {self.id_applic};''')[-1][0].split('-')
        last_num = int(last_name[0])
        last_y = int(last_name[2])

        query = ('''INSERT INTO report
        (name, applicat_id, type_work, method_id) VALUES (%s, %s, %s, %s);''')

        for i in range(len(logs)):
            name = f'{str(last_num)}-{logs[i]}-{str(last_y)}'
            val = (name, self.id_applic, typesWork[i], ids_met[i])
            self.db.query_insert(query, val)

        # Функция рассылки внутренней заявки исполнителям
    def send_mail(self, s_loc, ids_usr, name):
        self.s_loc = s_loc

        self.name = name
        self.get_connect()

        mail = Set_Mail()
        ids_usr = list(set(ids_usr))

        ids_usr = [str(i) for i in ids_usr]
        email_list = self.db.query(f'''SELECT email FROM user
        WHERE id IN ({",".join(ids_usr)});''')
        email_list = [email_list[i][0] for i in range(len(email_list))]
        subject = f'Заявка №{name}'
        filepath = self.s_loc
        text = f'''Добрый день! <br>Не нужно отвечать на это сообщение.<br>
        Вы являетесь исполнителем Заявки №{name}, которая находится
        во вложении.'''
        mail.sendMail(subject, email_list, text, filepath)
