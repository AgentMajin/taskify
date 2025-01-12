import sys
from PyQt5.QtWidgets import QApplication
from controllers.login_page import LoginController
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'controllers'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginController()  # Start with the login page
    login_window.show()
    sys.exit(app.exec_())