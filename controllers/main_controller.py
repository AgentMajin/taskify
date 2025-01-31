import sys
import os

from PyQt5 import QtGui
import platform


# Import icon file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources')))

# Show App icon on Taskbar (Windows only)
import ctypes

# Check if the operating system is not macOS & Linux
if platform.system() not in ["Darwin", "Linux"]:
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from datetime import date, datetime, timedelta
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFrame, QStyleFactory

# Add paths for importing custom modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'controllers'))

from ui.main_ui import Ui_MainWindow  # Import the generated UI class
from models.main_model import TaskModel  # Import the task model
# from task_frame import TaskFrame  # Import the custom task frame
from controllers.task_page import TaskPage  # Import the custom task page
from context import database as db
from context import localStorage

# Config date string
today = date.today()
# today = (date.today() + timedelta(days=1))
today_str = today.strftime("%d/%m/%Y")
tomorrow_str = (today + timedelta(days=1)).strftime('%d/%m/%Y')
cheating_space = "                                                  "
class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_task_id = None
        self.selected_menu_item = None
        self.previous_clicked_task = None

        # Config icon and app name
        self.setWindowTitle("Taskify")
        window_icon = QtGui.QIcon()
        window_icon.addPixmap(QtGui.QPixmap(":/icon/icons/check_fill.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(window_icon)

        # Initialize the TaskModel
        self.task_model = TaskModel()

        # Connect UI buttons to their respective methods
        self.ui.delete_task_button.clicked.connect(self.delete_task)  # Handle deleting a task
        self.ui.input_note.editingFinished.connect(self.add_note)  # Handle saving a note
        self.ui.due_date_input.dateChanged.connect(self.update_duedate)  # Handle due date updates
        self.ui.important_check.toggled.connect(self.update_important)  # Handle toggling importance
        self.ui.close_button.clicked.connect(self.close_page)
        self.ui.task_title_2.textChanged.connect(self.update_task_title)
        self.ui.done_check_3.toggled.connect(self.update_completed)
        self.ui.myday_check.toggled.connect(self.update_myday)
        self.ui.search_input.textChanged.connect(self.reload)
        self.ui.search_input.textChanged.connect(lambda: self.ui.task_details_frame.hide())
        self.ui.logout_button.clicked.connect(self.logout)

        # Initialize and add task pages
        self.init_task_pages()

        # Connect navigation buttons to change stacked widget pages
        self.ui.task_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.important_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.overdued_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.my_day_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))

        self.ui.task_button.clicked.connect(self.switch_page_effect)
        self.ui.important_button.clicked.connect(self.switch_page_effect)
        self.ui.overdued_button.clicked.connect(self.switch_page_effect)
        self.ui.my_day_button.clicked.connect(self.switch_page_effect)

        self.get_user_infor()
        self.ui.name_label.setText(self.user_name)
        self.ui.email_label.setText(self.user_email)

    def init_task_pages(self):
        """
        Initialize and add pages for different task views.
        """
        # All Tasks Page
        self.all_task_page = TaskPage(data_model=self.task_model,
                                      bg_url="url(:/icon/img/note-background.jpg)",
                                      title="All Tasks")
        self.ui.stackedWidget.addWidget(self.all_task_page)
        self.all_task_page.add_task_button.clicked.connect(self.reload)

        # Important Tasks Page
        self.important_task_page = TaskPage(data_model=self.task_model,
                                            bg_url="url(:/icon/img/important-bg.jpg)",
                                            title="Important Tasks",
                                            important_only=True)
        self.ui.stackedWidget.addWidget(self.important_task_page)
        self.important_task_page.add_task_button.clicked.connect(self.reload)

        # Overdue Tasks Page
        self.overdued_task = TaskPage(data_model=self.task_model,
                                      bg_url="url(:/icon/img/note-background-3.png)",
                                      title="Overdued Tasks",
                                      show_completed=False,
                                      overdued_only=True,
                                      allow_adding_task=False)
        self.ui.stackedWidget.addWidget(self.overdued_task)

        # Myday Tasks
        self.myday_task = TaskPage(data_model=self.task_model,
                                   bg_url="url(:/icon/img/important-bg-2.jpg)",
                                   title="My Day",
                                   myday=True)
        self.ui.stackedWidget.addWidget(self.myday_task)
        self.myday_task.add_task_button.clicked.connect(self.reload)

        # Load tasks into all pages
        self.load_all_tasks()

    def load_all_tasks(self):
        """
        Load tasks into each task page.
        """
        #
        if not self.ui.task_details_frame.isHidden():
            detail_task_id = self.current_task_id
        else:
            detail_task_id = None

        self.all_task_page.reload_task(
            task_clicked_callback=[self.update_task_details],
            task_updated_callback=[self.update_task_details, self.reload],
            detail_task_id = detail_task_id,
            search_keyword=self.ui.search_input.text()
        )

        self.important_task_page.reload_task(
            task_clicked_callback=[self.update_task_details],
            task_updated_callback=[self.update_task_details, self.reload],
            detail_task_id = detail_task_id,
            search_keyword=self.ui.search_input.text()
        )

        self.overdued_task.reload_task(
            task_clicked_callback=[self.update_task_details],
            task_updated_callback=[self.update_task_details, self.reload],
            detail_task_id = detail_task_id,
            search_keyword=self.ui.search_input.text()
        )

        self.myday_task.reload_task(
            task_clicked_callback=[self.update_task_details],
            task_updated_callback=[self.update_task_details, self.reload],
            detail_task_id = detail_task_id,
            search_keyword=self.ui.search_input.text()
        )

        self.previous_clicked_task = None

    def reload(self):
        """
        Reload tasks in all task pages.
        """
        self.load_all_tasks()

    def add_task(self):
        """
        Add a new task to the database and reload the task list.
        """
        task_title = self.ui.task_input_4.text().strip()
        if not task_title:
            QMessageBox.warning(self, "Error", "Task title cannot be empty!")
            return

        # Add the task to the database
        self.task_model.add_task(task_title)

        # Clear the input field
        self.ui.task_input_4.clear()

        # Reload the task list
        self.load_all_tasks()


    def clear_layout(self, layout):
        """
        Remove all widgets from a given layout.
        """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()  # Safely delete the widget

    def update_task_details(self, task_data):
        """
        Update the task details section with the selected task's information.
        """

        # Update due date information
        if task_data.get('due_date'):
            # Convert due date string to QDate and block signals to prevent unintended updates
            date_pyqt = QDate.fromString(task_data['due_date'], "dd/MM/yyyy")
            self.ui.due_date_input.blockSignals(True)
            self.ui.due_date_input.setDate(date_pyqt)
            self.ui.due_date_input.blockSignals(False)
        else:
            # Set default date if no due date is provided
            self.ui.due_date_input.blockSignals(True)
            self.ui.due_date_input.setDate(QDate(1970, 1, 1))
            self.ui.due_date_input.blockSignals(False)

        # Save current_task_id for updating Task details
        self.current_task_id = task_data['id']

        # Update Task Title (note: block signal to avoid calling the function update_task_title)
        self.ui.task_title_2.blockSignals(True)
        self.ui.task_title_2.setText(task_data['title'])
        self.ui.task_title_2.blockSignals(False)

        # Update to show if Task is in My Day list
        if (task_data['due_date'] == today_str or (task_data['is_myday'] == True and task_data['expired_date_myday'] == tomorrow_str)):
            self.ui.myday_check.blockSignals(True)
            self.ui.myday_check.setChecked(True)
            self.ui.myday_check.setText(" Added to My Day" + cheating_space)
            self.ui.myday_check.blockSignals(False)
        else:
            self.ui.myday_check.blockSignals(True)
            self.ui.myday_check.setChecked(False)
            self.ui.myday_check.setText(" Add to My Day" + cheating_space)
            self.ui.myday_check.blockSignals(False)

        # Update tto show if Task is marked as important
        self.ui.important_check.blockSignals(True)
        self.ui.important_check.setChecked(task_data['important'])
        self.ui.important_check.blockSignals(False)

        # Update to show if Task is completed
        self.ui.done_check_3.blockSignals(True)
        self.ui.done_check_3.setChecked(task_data['completed'])
        self.ui.done_check_3.blockSignals(False)

        # Update to show Task Description
        self.ui.input_note.blockSignals(True)
        self.ui.input_note.setText(task_data['description'])
        self.ui.input_note.blockSignals(False)

        # Update created date of the Task
        self.ui.created_date_label.setText(f"Created on {task_data['created_date']}")

        # If the Task Details Side Bar is hidden -> show it
        if self.ui.task_details_frame.isHidden():
            self.ui.task_details_frame.show()
        self.reload()

    def delete_task(self):
        """
        Delete the selected task from the database and reload the task list.
        """
        reply = QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.task_model.delete_task(self.current_task_id)
            QMessageBox.information(self, "Delete Task", "Task deleted!")
            self.load_all_tasks()
            self.ui.task_details_frame.hide()

    def add_note(self):
        """
        Save a note for the currently selected task.
        """
        note_text = self.ui.input_note.text().strip()
        current_note = self.task_model.get_a_task(self.current_task_id)
        current_note = current_note['description']
        if note_text != current_note:
            self.task_model.update_task(self.current_task_id, description=note_text)
            QMessageBox.information(self, "Description", "Your Description has been saved!")
            self.load_all_tasks()

    def update_duedate(self, newdate):
        """
        Update the due date for the currently selected task.
        """
        date_string = newdate.toString('dd/MM/yyyy')

        self.task_model.update_task(self.current_task_id, due_date=date_string)
        # Update to show if Task is in My Day list
        is_myday = self.task_model.get_a_task(self.current_task_id).get('is_myday')
        expired_date_myday = self.task_model.get_a_task(self.current_task_id).get('expired_date_myday')
        if is_myday and (expired_date_myday == tomorrow_str):
            pass
        elif (not self.ui.myday_check.isChecked()) and (date_string == today_str):
            self.ui.myday_check.setChecked(True)
            self.ui.myday_check.setText(" Added to My Day" + cheating_space)
        elif (self.ui.myday_check.isChecked()) and (date_string != tomorrow_str):
            self.ui.myday_check.setChecked(False)
            self.ui.myday_check.setText(" Add to My Day" + cheating_space)
        self.reload()

    def update_important(self):
        """
        Update the importance status for the currently selected task.
        """
        self.task_model.update_task(self.current_task_id, important=self.ui.important_check.isChecked())
        self.reload()

    def update_task_title(self):
        self.task_model.update_task(self.current_task_id, title=self.ui.task_title_2.text())
        self.reload()

    def update_completed(self):
        self.task_model.update_task(self.current_task_id, completed=self.ui.done_check_3.isChecked())
        self.reload()

    def update_myday(self):
        if self.ui.myday_check.isChecked():
            self.task_model.update_task(self.current_task_id, expired_date_myday=tomorrow_str)
            self.ui.myday_check.setText(" Added to My Day" + cheating_space)
        else:
            self.ui.myday_check.setText(" Add to My Day" + cheating_space)
        self.task_model.update_task(self.current_task_id, is_myday=self.ui.myday_check.isChecked())
        self.reload()

    def switch_page_effect(self):
        # Highlight selected item
        if self.selected_menu_item:
            frame_name = self.selected_menu_item.objectName()
            self.selected_menu_item.setStyleSheet(f"#{frame_name}::hover" + "{background-color: rgba(255, 255, 255, "
                                                  "0.8); \n}")

        sender = self.sender()
        parent_frame = sender.parent()
        parent_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.selected_menu_item = parent_frame

    def get_user_infor(self):
        user_id = localStorage.load_user_id()
        connection = db.connect_db()
        cursor = connection.execute("SELECT USERNAME, EMAIL FROM USERS WHERE UserId = ?",(user_id,))
        result = cursor.fetchall()
        self.user_name = result[0][0]
        self.user_email = result[0][1]

    def close_page(self):
        if self.ui.task_details_frame.isHidden():
            self.ui.task_details_frame.show()
        else:
            self.ui.task_details_frame.hide()

    def logout(self):
        from login_page import LoginController
        login = LoginController()
        login.show()
        self.hide()

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # Optional: Improve pixmap scaling

    app = QApplication(sys.argv)
    main_window = MainController()
    main_window.showMaximized()
    sys.exit(app.exec_())
