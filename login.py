from PyQt5 import QtWidgets


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('LabDocs')
        self.textLabel = QtWidgets.QLabel('Введите пароль', self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonLogin = QtWidgets.QPushButton('Войти', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textLabel)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if self.textPass.text() == '0000':    # Хы! Пароль! Сейчас уже пароль хранится в БД, сейчас он выствлен на показ для того, если Вы будете делать клон.
            self.accept()
        else:
            QtWidgets.QMessageBox.critical(
                self, 'Ошибка', 'Неверный пароль')
            self.textPass.setText('')
