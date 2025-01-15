'''
Sample Login Page (No logic added)
Run this Script to see the Login Page, if username = admin and password = admin, it will show "Login Successful" in the console.
Otherwise, it will show "Login Failed! Check your username and password" in the label.
'''

from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import sys
from context import database as db
from context import localStorage

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
            self.ui.label_3.setText("Login Successful")
            self.open_main_page()
        else:
            self.ui.label_3.setText("Login Failed! Check your username and password")
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()

    def validate_cred(self, username, password):
        connection = db.connect_db()
        cursor = connection.execute('SELECT * FROM Users u WHERE u.UserName = ? AND u.Password = ?', (username, password))
        result = cursor.fetchall()
        if(len(result) == 1):
            localStorage.userID = result[0][0]
            return True
        return False

    def open_main_page(self):
        from main_controller import MainController
        self.main_window = MainController()
        self.main_window.show()
        self.close()
        
if __name__ == "__main__":
    localStorage = QApplication(sys.argv)
    login = LoginController()
    login.show()
    sys.exit(localStorage.exec_())
