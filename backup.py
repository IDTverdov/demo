import os
import datetime
import random
import pandas as pd
from connect.connect import DataBase
from setting import SetupSetting


class BackUp(object):
    db = None
    setting = None

    def __init__(self):
        super().__init__()

    def get_connect(self):
        self.db = DataBase()

    def get_setting(self):
        self.setting = SetupSetting()

    def creatorDump(self):
        self.get_setting()
        path = self.setting.readReserv()
        d = str(datetime.datetime.now().date())
        os.system(f'''mysqldump.exe -u root -pPassword database > "{
            path.strip()}dump_{d}.sql"''')

    def creator_excel(self, ot, do):
        self.get_connect()
        # Договоры
        answ_contract = self.db.query(f'''SELECT DATE_FORMAT(date_start, '%d.%m.%Y'), number, client,
            phone, adress, DATE_FORMAT(date_end,'%d.%m.%Y') FROM contract
        WHERE date_start >= "{ot}" AND date_start <= "{do}";''')
        date_start, numbers_contract, clients = [], [], []
        date_end, adress, phone = [], [], []
        for i in range(len(answ_contract)):
            date_start.append(answ_contract[i][0])
            numbers_contract.append(answ_contract[i][1])
            clients.append(answ_contract[i][2])
            phone.append(answ_contract[i][3])
            adress.append(answ_contract[i][4])
            date_end.append(answ_contract[i][5])

        df_contract = pd.DataFrame(
            {'Дата начала Договора': date_start,
             'Номер договора': numbers_contract,
             'Наименование Заказчика': clients,
             'Телефон': phone, 'Адрес': adress,
             'Дата окончания Договора': date_end})

        # Заявки по Договорам
        answ_applic_contract = self.db.query(
            f'''SELECT DATE_FORMAT(date, '%d.%m.%Y'), applic_contract.number,
            contract.number, contract.client, price,
            IF(status = 0, 'Аннулировано',
            IF(status = 1, 'В работе', 'Выполнено'))
            FROM applic_contract
            JOIN contract ON applic_contract.contract_id = contract.id
            WHERE date >= "{ot}" AND date <= "{do}";''')
        date, numbers_applic_contract, contract = [], [], []
        clients, price, status = [], [], []
        for i in range(len(answ_applic_contract)):
            date.append(answ_applic_contract[i][0])
            numbers_applic_contract.append(answ_applic_contract[i][1])
            contract.append(answ_applic_contract[i][2])
            clients.append(answ_applic_contract[i][3])
            price.append(answ_applic_contract[i][3])
            status.append(answ_applic_contract[i][5])
        df_applic_contract = pd.DataFrame(
            {'Дата Заявки по Договору': date,
             'Номер Заявки': numbers_applic_contract,
             'по Договору': contract,
             'Наименование Заказчика': clients,
             'Стоимость (с НДС), \n рублей': price,
             'Статус': status})

        # Пробы
        answ_sample = self.db.query(f'''SELECT sample.id,
            DATE_FORMAT(sample.date,'%d.%m.%Y'), sample.number,
            sample.name, applicat.name,sample.type,
            CONCAT_WS(', ', contract.number, contract.client),
            GROUP_CONCAT(DISTINCT type_method.name ORDER BY 1 SEPARATOR ', '),
            sample.info
            FROM sample
            JOIN applicat ON applicat.id = sample.applicat_id
            JOIN applicat_has_uhtm ON
                applicat_has_uhtm.applicat_id = applicat.id
            JOIN user_has_type_method ON
            applicat_has_uhtm.user_has_type_method_id = user_has_type_method.id
            JOIN type_method
                ON user_has_type_method.type_method_id = type_method.id
            JOIN contract ON applicat.contract_id = contract.id
            WHERE sample.date >= "{ot}" AND sample.date <= "{do}"
            GROUP BY 1 ORDER BY 1;''')

        date_sample, number_sample, name_sample, = [], [], []
        num_applic_sample, type_sample, clients = [], [], []
        type_work, info_sample = [], []
        for i in range(len(answ_sample)):
            date_sample.append(answ_sample[i][1])
            number_sample.append(answ_sample[i][2])
            name_sample.append(answ_sample[i][3])
            num_applic_sample.append(answ_sample[i][4])
            type_sample.append(answ_sample[i][5])
            clients.append(answ_sample[i][6])
            type_work.append(answ_sample[i][7])
            info_sample.append(answ_sample[i][8])

        df_sample = pd.DataFrame(
            {'Дата поступления': date_sample,
             'Лабораторный номер': number_sample,
             'Наименование образца Заказчика': name_sample,
             'Номер Заявки': num_applic_sample,
             'Описание пробы': type_sample,
             'Договор, Заказчик': clients,
             'Методы испытаний': type_work,
             'Примечания': info_sample})

        # Заявки
        answ_applic = self.db.query(f'''SELECT DATE_FORMAT(applicat.date,'%d.%m.%Y'),
        report.name, (SELECT name FROM method WHERE id = report.method_id),
        type_work,
        (SELECT number FROM contract WHERE id = applicat.contract_id),
        (SELECT number FROM applic_contract
        WHERE id = applicat.applic_contract_id),
        (SELECT date FROM applic_contract
            WHERE id = applicat.applic_contract_id),
        IF(status = 0, 'Аннулировано',
        IF(report.date IS null, 'В работе', 'Выполнено')),
        DATE_FORMAT(report.date, '%d.%m.%Y'),
        (GROUP_CONCAT(DISTINCT sample.number ORDER BY 1 SEPARATOR ', '))
        FROM report
        JOIN applicat ON applicat.id = applicat_id
        JOIN sample ON applicat.id = sample.applicat_id
        JOIN sample_has_method ON sample_has_method.sample_id = sample.id
        WHERE sample_has_method.method_id = report.method_id AND
        applicat.date >= "{ot}" AND applicat.date <= "{do}"
        GROUP BY 1''')
        date_applicat, name_applicat, method = [], [], []
        type_work, contract, applic_contract = [], [], []
        date_applic_contract = []
        status, date_report, lab_nums = [], [], []
        for i in range(len(answ_applic)):
            date_applicat.append(answ_applic[i][0])
            name_applicat.append(answ_applic[i][1])
            method.append(answ_applic[i][2])
            type_work.append(answ_applic[i][3])
            contract.append(answ_applic[i][4])
            applic_contract.append(answ_applic[i][5])
            date_applic_contract.append(answ_applic[i][6])
            status.append(answ_applic[i][7])
            date_report.append(answ_applic[i][8])
            lab_nums.append(answ_applic[i][9])
        df_applicat = pd.DataFrame(
            {'Дата Заявки': date_applicat, 'Номер Заявки': name_applicat,
             'Метод анализа': method, 'Виды работ': type_work,
             'Номер Договора': contract,
             'Номер Заявки по Договру': applic_contract,
             'Дата Заявки по Договру': date_applic_contract,
             'Статус': status, 'Дата выполнения/аннулирования': date_report,
             'Лабораторные номера': lab_nums})

        # Запись в файл
        self.get_setting()
        path = self.setting.readReserv()
        name = path.strip() + f'labdocs_{ot}_{do}.xlsx'
        dates = {'Договоры': df_contract,
                 'Заявки по Договорам': df_applic_contract,
                 'Заявки': df_applicat, 'Пробы': df_sample}
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        for sheet_name in dates.keys():
            dates[sheet_name].to_excel(
                 writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column('A:J', 15)
            password = random.randint(1000, 9999)
            worksheet.protect(password)
        writer.save()

    def autorun(self):
        self.get_setting()
        pathn = self.setting.readReserv()
        datenow = datetime.datetime.now().date()
        files = os.listdir(pathn.strip())
        dumps = []
        for i in files:
            if 'dump_' in i:
                d = i[5:-4]
                dumps.append(d)
        if dumps != []:
            datelast = datetime.datetime.strptime(
                 max(dumps), "%Y-%m-%d").date()
            if (datenow - datelast).days >= 90:
                self.creatorDump()
                self.creator_excel(str(datelast), str(datenow))
        else:
            self.creatorDump()
            self.creator_excel('2022-01-01', str(datenow))
