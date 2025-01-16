'''
Sample Login Page (No logic added)
Run this Script to see the Login Page, if username = admin and password = admin, it will show "Login Successful" in the console.
Otherwise, it will show "Login Failed! Check your username and password" in the label.
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import sys
from context import database as db
from context import localStorage

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ui import login_ui_2

class LoginController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = login_ui_2.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.login_button.clicked.connect(self.authenticate)

        # Switch between sign in, sign up, reset password pages as user click buttons
        self.ui.go_to_signup_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.go_to_signup.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.back_to_login_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.back_to_login.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.go_to_reset_pass_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.go_to_reset_pass.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

    def authenticate(self):
        username = self.ui.username_input_2.text()
        password = self.ui.pass_input_3.text()

        if self.validate_cred(username, password):
            print("Login Successful")
            self.ui.notify_message_3.setText("Login Successful")
            self.open_main_page()
        else:
            self.ui.notify_message_3.setText("Login Failed! Check your username and password")
            self.ui.username_input_2.clear()
            self.ui.pass_input_3.clear()

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

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # Optional: Improve pixmap scaling

    localStorage = QApplication(sys.argv)
    login = LoginController()
    login.showMaximized()
    sys.exit(localStorage.exec_())
