import sys
from PyQt5.QtWidgets import QApplication
from controllers.login_page import LoginController
from controllers.main_controller import MainController
import os
from PyQt5 import QtGui

sys.path.append(os.path.join(os.path.dirname(__file__), 'controllers'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_icon = QtGui.QIcon()
    window_icon.addPixmap(QtGui.QPixmap(":/icon/icons/check_fill.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    app.setWindowIcon(window_icon)
    login_window = LoginController()  # Start with the login page
    login_window.show()

    sys.exit(app.exec_())