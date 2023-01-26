# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from applic_in import Ui_Applic
from applic_knitu_in import Applic_KNITU
from contract import Ui_Contract
from report import Ui_Report
from source import Ui_Source
from insert_sample import Ui_Insert_samples
from usrs import Ui_Usrs
from show_log import Log
from setting import SetupSetting
# from backup import BackUp


class MainWindowManager(object):
    mainWindow = None
    centralWidget = None
    subWidget = None

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

    # def autoback(self):
    #     '''Запуск автоматичского бэкапа'''
    #     bk = BackUp()
    #     bk.autorun()

    def show(self):
        '''Запуск всех методов'''
        self.setupWindow()
        self.centralWidget = QtWidgets.QWidget(self.mainWindow)
        self.setupCentralWidget(self.centralWidget)
        self.setupHomePage()
        self.mainWindow.show()
        # self.autoback()

    def setupWindow(self):
        '''Настройка главного окна'''
        self.mainWindow.resize(1070, 760)
        self.mainWindow.setWindowTitle("myProject")
        menubar = QtWidgets.QMenuBar(self.mainWindow)
        menubar.setGeometry(QtCore.QRect(0, 0, 1070, 20))
        self.mainWindow.setMenuBar(menubar)
        menuFile = QtWidgets.QMenu(menubar)
        menuFile.setTitle("Файл")
        menuFile.addAction("Главная", self.setupHomePage)
        menuFile.addAction("Последние действия", self.showLog)
        menuFile.addAction("Настройки", self.setupSetting)
        menuFile.addAction('Выход', self.mainWindow.close)
        menubar.addAction(menuFile.menuAction())
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)

    def setupCentralWidget(self, widget):
        self.mainWindow.setCentralWidget(widget)

    def setupSubWidget(self):
        if self.subWidget is None:
            self.subWidget = QtWidgets.QWidget(self.centralWidget)
        else:
            self.subWidget.hide()
            self.subWidget = QtWidgets.QWidget(self.centralWidget)
        self.subWidget.setGeometry(QtCore.QRect(250, 140, 770, 550))
        return self.subWidget

    def setupHomePage(self):
        self.centralWidget = QtWidgets.QWidget(self.mainWindow)
        self.setupCentralWidget(self.centralWidget)
        self.subWidget = None
        self.setupSubWidget()
        # Фон
        bgImage = QtWidgets.QLabel(self.centralWidget)
        bgImage.setGeometry(QtCore.QRect(-20, 0, 1111, 751))
        bgImage.setPixmap(QtGui.QPixmap("title.png"))

        # Кнопки для переключения виджетов
        btnApplicat = QtWidgets.QPushButton(self.centralWidget)
        btnApplicat.setGeometry(QtCore.QRect(5, 220, 235, 30))
        btnApplicat.setText("Заявки")
        btnApplicat.clicked.connect(self.applicatWidget)
        btnUsrs = QtWidgets.QPushButton(self.centralWidget)
        btnUsrs.setText("Сотрудники")
        btnUsrs.setGeometry(QtCore.QRect(5, 260, 235, 30))
        btnUsrs.clicked.connect(self.usersWidget)
        btnReserv = QtWidgets.QPushButton(self.centralWidget)
        btnReserv.setGeometry(QtCore.QRect(5, 300, 235, 30))
        btnReserv.setText("Резервное копирование")
        btnReserv.clicked.connect(self.reservWidget)
        self.applicatWidget()

    def applicatWidget(self):
        self.setupSubWidget()

        btnContract = QtWidgets.QPushButton(self.subWidget)
        btnContract.setGeometry(QtCore.QRect(140, 120, 180, 30))
        btnContract.clicked.connect(self.newContract)
        btnContract.setText("Внести данные Договора")
        btnApplicat = QtWidgets.QPushButton(self.subWidget)
        btnApplicat.setGeometry(QtCore.QRect(340, 160, 180, 30))
        btnApplicat.clicked.connect(self.newApplicat)
        btnApplicat.setText("Сформировать Заявку")
        btnApplicat_KN = QtWidgets.QPushButton(self.subWidget)
        btnApplicat_KN.setGeometry(QtCore.QRect(340, 120, 180, 30))
        btnApplicat_KN.clicked.connect(self.newApplicat_KN)
        btnApplicat_KN.setText("Внести Заявку по Договору")
        btnReport = QtWidgets.QPushButton(self.subWidget)
        btnReport.setGeometry(QtCore.QRect(140, 200, 180, 30))
        btnReport.clicked.connect(self.newReport)
        btnReport.setText("Сформировать Протокол")
        btnSample = QtWidgets.QPushButton(self.subWidget)
        btnSample.setGeometry(QtCore.QRect(140, 160, 180, 30))
        btnSample.clicked.connect(self.insertSamples)
        btnSample.setText("Внести образцы")
        btnSource = QtWidgets.QPushButton(self.subWidget)
        btnSource.setGeometry(QtCore.QRect(340, 200, 180, 30))
        btnSource.clicked.connect(self.source)
        btnSource.setText("ПРОСМОТР")
        titleApplicat = QtWidgets.QLabel(self.subWidget)
        titleApplicat.setGeometry(QtCore.QRect(275, 40, 120, 30))
        titleApplicat.setText("Заявки")
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        titleApplicat.setFont(font)
        self.subWidget.show()

    def reservWidget(self):
        self.setupSubWidget()
        titleReserv = QtWidgets.QLabel(self.subWidget)
        titleReserv.setText("Управление резервным копированием")
        titleReserv.setGeometry(QtCore.QRect(130, 40, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        titleReserv.setFont(font)
        labelReserv = QtWidgets.QLabel(self.subWidget)
        labelReserv.setText("Выберите период для копирования")
        btn_reserv_start = QtWidgets.QPushButton(self.subWidget)
        btn_reserv_start.setGeometry(QtCore.QRect(260, 260, 131, 41))
        btn_reserv_start.setText("Создать копию")
        btn_reserv_start.clicked.connect(lambda: self.get_reserv())
        self.date_ot = QtWidgets.QDateEdit(self.subWidget)
        self.date_ot.setGeometry(QtCore.QRect(200, 190, 110, 22))
        self.date_ot.setDisplayFormat("d.M.yyyy")
        self.date_do = QtWidgets.QDateEdit(self.subWidget)
        self.date_do.setGeometry(QtCore.QRect(350, 190, 110, 22))
        self.date_do.setDisplayFormat("d.M.yyyy")
        labelReserv.setGeometry(QtCore.QRect(230, 130, 191, 31))
        reserv_label_ot = QtWidgets.QLabel(self.subWidget)
        reserv_label_ot.setGeometry(QtCore.QRect(180, 190, 21, 21))
        reserv_label_ot.setText("От")
        reserv_label_do = QtWidgets.QLabel(self.subWidget)
        reserv_label_do.setGeometry(QtCore.QRect(330, 190, 21, 21))
        reserv_label_do.setText("до")
        self.reserv_mess = QtWidgets.QLabel(self.subWidget)
        self.reserv_mess.setGeometry(QtCore.QRect(240, 320, 200, 41))
        self.subWidget.show()

    def usersWidget(self):
        self.setupSubWidget()
        usrs = Ui_Usrs()
        usrs.show(self.subWidget, self.setupSubWidget,
                  self.btnBckToUsr, self.mainWindow)
        self.subWidget.show()

    def setupWorkPage(self):
        self.centralWidget = QtWidgets.QWidget(self.mainWindow)
        self.setupCentralWidget(self.centralWidget)
        self.btnBckToHomePage(self.centralWidget)

    def showLog(self):
        self.setupWorkPage()
        sl = Log()
        sl.showLog(self.centralWidget)

    def setupSetting(self):
        self.setupWorkPage()
        sset = SetupSetting()
        sset.windowSetting(self.centralWidget)

    def newApplicat(self):
        self.setupSubWidget()
        uapp = Ui_Applic()
        uapp.applic(self.subWidget, self.btnBckToApplicat, self.mainWindow)
        self.subWidget.show()

        # окно добавления договора
    def newContract(self):
        self.setupSubWidget()
        ucon = Ui_Contract()
        ucon.contract(self.subWidget, self.btnBckToApplicat)
        self.subWidget.show()

        # окно создания протокола
    def newReport(self):
        self.setupSubWidget()
        urep = Ui_Report()
        urep.report(self.subWidget, self.btnBckToApplicat)
        self.subWidget.show()

        # окно внесения образцов
    def insertSamples(self):
        self.setupSubWidget()
        uis = Ui_Insert_samples()
        uis.insert_samples(self.subWidget, self.btnBckToApplicat)
        self.subWidget.show()

        # окно просмотра
    def source(self):
        self.centralWidget = QtWidgets.QWidget(self.mainWindow)
        self.setupCentralWidget(self.centralWidget)
        usou = Ui_Source()
        usou.source(self.setupCentralWidget, self.btnBckToHomePage)

    def btnBckToApplicat(self, widget):
        btnBckToApplicat = QtWidgets.QPushButton(widget)
        btnBckToApplicat.setGeometry(QtCore.QRect(5, 5, 100, 30))
        btnBckToApplicat.setText("Назад")
        btnBckToApplicat.clicked.connect(self.applicatWidget)

    def btnBckToHomePage(self, widget):
        btnHome = QtWidgets.QPushButton(widget)
        btnHome.setGeometry(QtCore.QRect(20, 20, 100, 30))
        btnHome.setText('Главная')
        btnHome.clicked.connect(self.setupHomePage)

    def btnBckToUsr(self, widget):
        btn = QtWidgets.QPushButton(widget)
        btn.setGeometry(QtCore.QRect(5, 5, 100, 30))
        btn.setText("Назад")
        btn.clicked.connect(self.usersWidget)

    def get_reserv(self):
        ot = '-'.join(self.date_ot.text().split('.')[::-1])
        do = '-'.join(self.date_do.text().split('.')[::-1])
        if ot == '2000-1-1':
            self.reserv_mess.setText('Выберете начальную дату')
        elif do == '2000-1-1':
            self.reserv_mess.setText('Выберете конечную дату')
        else:
            # bk = BackUp()
            # bk.creator_excel(ot, do)
            # bk.creatorDump()
            self.reserv_mess.setText(f'''             Сохранён файл
            \nlabdocs_{ot}_{do}''')

    def newApplicat_KN(self):
        self.setupSubWidget()
        uappkn = Applic_KNITU()
        uappkn.applic_knitu(self.subWidget, self.btnBckToApplicat)
        self.subWidget.show()
