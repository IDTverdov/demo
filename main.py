# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from mw import MainWindowManager
from login import Login

app = QtWidgets.QApplication(sys.argv)
login = Login()
if login.exec_() == QtWidgets.QDialog.Accepted:
    mainWindow = QtWidgets.QMainWindow()
    mwm = MainWindowManager(mainWindow)
    mwm.show()
    sys.exit(app.exec_())
