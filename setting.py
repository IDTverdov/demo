# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from connect.connect import DataBase


class SetupSetting():
    dirApplic = None
    dirApplicUsr = None
    dirReport = None
    dirReserv = None
    db = None

    def __init__(self):
        super().__init__()

    def get_connect(self):
        self.db = DataBase()
        self.db.connect()

    def readTxt(self):
        with open('parametres.txt', 'r', encoding='utf-8') as f:
            listParametres = f.readlines()
            self.dirApplic = listParametres[0]
            self.dirApplicUsr = listParametres[1]
            self.dirReport = listParametres[2]
            self.dirReserv = listParametres[3]

    def readReport(self):
        self.readTxt()
        return self.dirReport

    def readReserv(self):
        self.readTxt()
        return self.dirReserv

    def writeTxt(self, dA=None, dAU=None, dR=None, dRz=None):
        if dA is None:
            dA = self.dirApplic.strip()
        if dAU is None:
            dAU = self.dirApplicUsr.strip()
        if dR is None:
            dR = self.dirReport.strip()
        if dRz is None:
            dRz = self.dirReserv.strip()

        listString = [dA+'\n', dAU+'\n', dR+'\n', dRz+'\n']

        with open('parametres.txt', 'w', encoding='utf-8') as f:
            f.writelines(listString)

    def windowSetting(self, widget):
        self.readTxt()
        # self.get_connect()
        self.dirApplic = self.dirApplic.strip()
        self.dirApplicUsr = self.dirApplicUsr.strip()
        self.dirReport = self.dirReport.strip()

        title = QtWidgets.QLabel(widget)
        title.setGeometry(QtCore.QRect(450, 100, 300, 30))
        title.setText('Настройки')
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)

        dirApplicLabel = QtWidgets.QLabel(widget)
        dirApplicLabel.setGeometry(QtCore.QRect(150, 200, 100, 20))
        dirApplicLabel.setText('Папка с Заявками')
        dirApplicLine = QtWidgets.QLineEdit(widget)
        dirApplicLine.setGeometry(QtCore.QRect(250, 200, 550, 20))
        dirApplicLine.setText(self.dirApplic)
        dirApplicLine.setReadOnly(True)
        btnApplic = QtWidgets.QPushButton(widget)
        btnApplic.setGeometry(QtCore.QRect(820, 195, 100, 30))
        btnApplic.setText('Изменить папку')
        btnApplic.clicked.connect(lambda: self.readLines(dirApplicLine))

        dirApplicUsrLabel = QtWidgets.QLabel(widget)
        dirApplicUsrLabel.setGeometry(QtCore.QRect(70, 250, 200, 20))
        dirApplicUsrLabel.setText('Папка с Заданиями на Испытания')
        dirApplicUsrLine = QtWidgets.QLineEdit(widget)
        dirApplicUsrLine.setGeometry(QtCore.QRect(250, 250, 550, 20))
        dirApplicUsrLine.setText(self.dirApplicUsr)
        dirApplicUsrLine.setReadOnly(True)
        btnApplicUsr = QtWidgets.QPushButton(widget)
        btnApplicUsr.setGeometry(QtCore.QRect(820, 245, 100, 30))
        btnApplicUsr.setText('Изменить папку')
        btnApplicUsr.clicked.connect(lambda: self.readLines(dirApplicUsrLine))

        dirReportLabel = QtWidgets.QLabel(widget)
        dirReportLabel.setGeometry(QtCore.QRect(130, 300, 120, 20))
        dirReportLabel.setText('Папка с Протоколами')
        dirReportLine = QtWidgets.QLineEdit(widget)
        dirReportLine.setGeometry(QtCore.QRect(250, 300, 550, 20))
        dirReportLine.setText(self.dirReport)
        dirReportLine.setReadOnly(True)
        btnReport = QtWidgets.QPushButton(widget)
        btnReport.setGeometry(QtCore.QRect(820, 295, 100, 30))
        btnReport.setText('Изменить папку')
        btnReport.clicked.connect(lambda: self.readLines(dirReportLine))

        dirReservLabel = QtWidgets.QLabel(widget)
        dirReservLabel.setGeometry(QtCore.QRect(97, 350, 150, 20))
        dirReservLabel.setText('Папка с Резерными копиями')
        dirReservLine = QtWidgets.QLineEdit(widget)
        dirReservLine.setGeometry(QtCore.QRect(250, 350, 550, 20))
        dirReservLine.setText(self.dirReserv)
        dirReservLine.setReadOnly(True)
        btnReserv = QtWidgets.QPushButton(widget)
        btnReserv.setGeometry(QtCore.QRect(820, 345, 100, 30))
        btnReserv.setText('Изменить папку')
        btnReserv.clicked.connect(lambda: self.readLines(dirReservLine))

        btnSave = QtWidgets.QPushButton(widget)
        btnSave.setGeometry(QtCore.QRect(455, 400, 100, 30))
        btnSave.setText('Сохранить')
        btnSave.clicked.connect(
            lambda: self.saveChange(dirApplicLine.text().strip(),
                                    dirApplicUsrLine.text().strip(),
                                    dirReportLine.text().strip(),
                                    dirReservLine.text().strip()))

        self.textMess = QtWidgets.QLabel(widget)
        self.textMess.setGeometry(QtCore.QRect(480, 450, 100, 30))

        # volume = self.db.query('''SELECT table_schema AS "Database Name",
        # ROUND(SUM(data_length + index_length) / 1024 / 1024, 2)
        # AS "Size in (MB)" FROM information_schema.TABLES
        # WHERE table_schema = "docslab"
        # GROUP BY table_schema;''')[0][1]

        # volumeText = 'Занимаемый объём ' + str(volume) + 'MB'
        # volumeLabel = QtWidgets.QLabel(widget)
        # volumeLabel.setGeometry(QtCore.QRect(100, 600, 140, 20))
        # volumeLabel.setText(volumeText)

    def saveChange(self, dA, dAU, dR, dRz):
        self.get_connect()
        if dA != self.dirApplic:
            self.dirApplic = dA
            self.writeTxt(dA=self.dirApplic)
            self.textMess.setText('Сохранено')
            queryLog = 'Изменена папка сохранения Заявок'
            self.db.insert_log(queryLog)

        if dAU != self.dirApplicUsr:
            self.dirApplicUsr = dAU
            self.writeTxt(dAU=self.dirApplicUsr)
            self.textMess.setText('Сохранено')
            queryLog = 'Изменена папка сохранения Заданий на испытания'
            self.db.insert_log(queryLog)

        if dRz != self.dirReserv:
            self.dirReserv = dRz
            self.writeTxt(dRz=self.dirReserv)
            self.textMess.setText('Сохранено')
            queryLog = 'Изменена папка сохранения Резервных копий'
            self.db.insert_log(queryLog)

        if dR != self.dirReport:
            self.dirReport = dR
            self.writeTxt(dR=self.dirReport)
            self.textMess.setText('Сохранено')
            queryLog = 'Изменена папка сохранения Протоколов'
            self.db.insert_log(queryLog)

    @QtCore.pyqtSlot()
    def readLines(self, line):
        loc = line.text()
        fwin = QtWidgets.QMainWindow()
        fname = QtWidgets.QFileDialog.getExistingDirectory(
            fwin, 'Выбрать папку', loc)
        fname = fname.replace('/', '\\')
        fname = fname + '\\'
        line.setText(fname)
