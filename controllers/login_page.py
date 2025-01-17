'''
Sample Login Page (No logic added)
Run this Script to see the Login Page, if username = admin and password = admin, it will show "Login Successful" in the console.
Otherwise, it will show "Login Failed! Check your username and password" in the label.
'''
import platform
import re

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import sys
from context import database as db
from context import localStorage

import ctypes


# Check if the operating system is not macOS & Linux
if platform.system() not in ["Darwin", "Linux"]:
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ui import login_ui_2

class LoginController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = login_ui_2.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Taskify")


        self.ui.login_button.clicked.connect(self.authenticate_login)
        self.ui.signup_button.clicked.connect(self.authenticate_signup)
        self.ui.reset_pass_btn.clicked.connect(self.authenticate_change_pass)

        # Switch between sign in, sign up, reset password pages as user click buttons
        self.ui.go_to_signup_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.go_to_signup.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.back_to_login_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.back_to_login.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.go_to_reset_pass_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.go_to_reset_pass.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

    def authenticate_login(self):
        username = self.ui.username_input_2.text()
        password = self.ui.pass_input_3.text()

        if self.validate_cred_login(username, password):
            self.ui.notify_message_3.setText("Login Successful")
            self.open_main_page()
        else:
            self.ui.notify_message_3.setText("Login Failed! Check your username and password")
            self.ui.username_input_2.clear()
            self.ui.pass_input_3.clear()

    def validate_cred_login(self, username, password):
        connection = db.connect_db()
        cursor = connection.execute('SELECT * FROM Users u WHERE u.UserName = ? AND u.Password = ?', (username, password))
        result = cursor.fetchall()
        if(len(result) == 1):
            # localStorage.userID = result[0][0]
            user_id = result[0][0]
            localStorage.save_user_id(user_id=user_id)
            return True
        return False

    def authenticate_signup(self):
        self.new_username = self.ui.username_input.text()
        self.new_password = self.ui.pass_input.text()
        self.new_password_confirm = self.ui.confirm_pass_input.text()
        self.new_email = self.ui.email_input.text()

        result_message = {1: "Account Created! Please go back to Sign in",
                          2: "Please don't leave any field blank and try again.!",
                          3: "Confirm Password failed! Please try again.",
                          4: "Username existed! Please try again.",
                          5: "Please check your email format again.",
                          6: "Your email is registered with another account! Please try again.",
                          7: "Something wrong happened! Please try again later.",}
        # Validate user input
        result_code, result_bool = self.validate_new_user()

        if result_bool:
            if self.insert_new_user():
                # Success
                self.ui.notify_message.setText(result_message[1])
                # Clear input fields if successful signup
                self.ui.username_input.clear()
                self.ui.pass_input.clear()
                self.ui.confirm_pass_input.clear()
                self.ui.email_input.clear()
            else:
                # Failed insertion
                self.ui.notify_message.setText(result_message[7])
        else:
            # Validation failed
            self.ui.notify_message.setText(result_message[result_code])


    def validate_new_user(self):
        connection = db.connect_db()
        if self.new_username == "" or self.new_password == "" or self.new_password_confirm == "" or self.new_email == "":
            return 2, False
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.new_email):
            return 5, False
        cursor = connection.execute('SELECT * FROM Users U WHERE u.UserName = ?', (self.new_username,))
        user = cursor.fetchall()
        if(len(user) >= 1):
            return 4, False
        cursor_2 = connection.execute('SELECT * FROM Users U WHERE u.Email = ?', (self.new_email,))
        email = cursor_2.fetchall()
        if(len(email) >= 1):
            return 6, False
        if self.new_password != self.new_password_confirm:
            return 3, False
        else:
            return 1, True

    def insert_new_user(self):
        connection = db.connect_db()
        try:
            # Execute the insert query
            cursor = connection.execute(
                "INSERT INTO Users (UserName, Password, Email) VALUES (?, ?, ?)",
                (self.new_username, self.new_password, self.new_email)
            )
            # Commit the transaction
            connection.commit()
            return True
        except Exception as e:
            # Log the error for debugging
            print(f"Error inserting new user: {e}")
            return False

    def authenticate_change_pass(self):
        self.username_change_pass = self.ui.username.text()
        self.current_pass = self.ui.current_pass_input.text()
        self.pass_to_change = self.ui.new_pass_input.text()
        self.pass_to_change_cf = self.ui.confirm_pass_input_2.text()

        result_message = {1: "Password changed! Please go back to Sign in",
                          2: "Please don't leave any field blank and try again.!",
                          3: "Confirm Password doesn't match! Please try again.",
                          4: "Current Password wrong! Please try again",
                          5: "Username doesn't exist! Please try again",
                          6: "Something wrong happened! Please try again later.",}

        # Validate user input
        result_code, result_bool = self.validate_change_pass()

        if result_bool:
            if self.change_pass():
                # Success
                self.ui.notify_message_2.setText(result_message[1])
                # Clear input fields if successful signup
                self.ui.username.clear()
                self.ui.current_pass_input.clear()
                self.ui.new_pass_input.clear()
                self.ui.confirm_pass_input_2.clear()
            else:
                # Failed insertion
                self.ui.notify_message_2.setText(result_message[6])
        else:
            # Validation failed
            self.ui.notify_message_2.setText(result_message[result_code])

    def validate_change_pass(self):
        connection = db.connect_db()
        if self.username_change_pass == "" or self.current_pass == "" or self.pass_to_change == "" or self.pass_to_change_cf == "":
            return 2, False
        cursor = connection.execute('SELECT * FROM Users U WHERE u.UserName = ?', (self.username_change_pass,))
        user = cursor.fetchall()
        if (len(user) == 0):
            return 5, False
        cursor_2 = connection.execute('SELECT Password FROM Users U WHERE u.UserName = ?', (self.username_change_pass,))
        password = cursor_2.fetchall()
        if (password[0][0] != self.current_pass):
            return 4, False
        if self.pass_to_change != self.pass_to_change_cf:
            return 3, False
        else:
            return 1, True

    def change_pass(self):
        connection = db.connect_db()
        try:
            # Execute the insert query
            cursor = connection.execute(
                "UPDATE Users SET Password = ? WHERE UserName = ? ",
                (self.pass_to_change, self.username_change_pass)
            )
            # Commit the transaction
            connection.commit()
            return True
        except Exception as e:
            # Log the error for debugging
            print(f"Error updating password: {e}")
            return False

    def open_main_page(self):
        from main_controller import MainController
        self.main_window = MainController()
        self.main_window.show()
        self.hide()
        
if __name__ == "__main__":

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # Optional: Improve pixmap scaling

    app = QApplication(sys.argv)
    login = LoginController()
    login.showMaximized()
    sys.exit(app.exec_())
