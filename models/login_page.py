from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ui import login_ui

class LoginController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = login_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.login_button.clicked.connect(self.authenticate)

    def authenticate(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        if self.validate_cred(username, password):
            print("Login Successful")
            self.accept()
        else:
            self.ui.label_3.setText("Login Failed! Check your username and password")
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
    
    def validate_cred(self, username, password):
        if username == "admin" and password == "admin":
            return True
        return False
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginController()
    login.show()
    sys.exit(app.exec_())
