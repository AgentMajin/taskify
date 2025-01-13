import sys
import os
from datetime import date, datetime

from PyQt5.QtCore import QObject, Qt, pyqtSignal, QDate

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFrame
from ui.main_ui import Ui_MainWindow  # Import the generated UI class
from models.main_model import TaskModel  # Import the task model
from task_frame import TaskFrame  # Import the custom task frame
from task_page import TaskPage


class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_task_id = None

        # Initialize the TaskModel
        self.task_model = TaskModel()

        # Connect UI buttons to their respective methods
        self.ui.add_task_button.clicked.connect(self.add_task)
        self.ui.delete_task_button.clicked.connect(self.delete_task)
        self.ui.input_note.editingFinished.connect(self.add_note)
        self.ui.due_date_input.dateChanged.connect(self.update_duedate)
        self.ui.add_check.toggled.connect(self.update_important)

        # Init Task Pages
        self.init_task_pages()

        self.ui.task_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.important_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.my_day_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))

    def init_task_pages(self):
        self.all_task_page = TaskPage(data_model=self.task_model,
                                      bg_url="url(:/icon/img/note-background.jpg)",
                                      title="All Tasks")
        self.ui.stackedWidget.addWidget(self.all_task_page)
        self.all_task_page.add_task_button.clicked.connect(self.reload)

        self.important_task_page = TaskPage(data_model=self.task_model,
                                            bg_url="url(:/icon/img/important-bg.jpg)",
                                            title="Important Tasks",
                                            important_only=True)
        self.ui.stackedWidget.addWidget(self.important_task_page)
        self.important_task_page.add_task_button.clicked.connect(self.reload)

        self.overdued_task = TaskPage(data_model=self.task_model,
                                      bg_url="url(:/icon/img/note-background-3.png)",
                                      title="Overdued Tasks",
                                      show_completed=False)
        self.ui.stackedWidget.addWidget(self.overdued_task)
        self.overdued_task.add_task_button.clicked.connect(self.reload)

        self.load_all_tasks()

    def load_all_tasks(self):
        """
        Load tasks from the database and display them in the all task list widget.
        """
        self.all_task_page.reload_task(
                              task_clicked_callback=self.update_task_details,
                              task_updated_callback=[self.update_task_details, self.reload])

        self.important_task_page.reload_task(
                              task_clicked_callback=self.update_task_details,
                              task_updated_callback=[self.update_task_details, self.reload])

        self.overdued_task.reload_task(
                              task_clicked_callback=self.update_task_details,
                              task_updated_callback=[self.update_task_details, self.reload])


    def reload(self):
        self.load_all_tasks()

    def add_task(self):
        """
        Add a new task to the database and update the task list widget.
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
        Remove all widgets from a layout.
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
        if task_data.get('due_date'):
            date_pyqt = QDate.fromString(task_data['due_date'], "dd/MM/yyyy")
            self.ui.due_date_input.blockSignals(True)
            self.ui.due_date_input.setDate(date_pyqt)
            self.ui.due_date_input.blockSignals(False)
        else:
            self.ui.due_date_input.blockSignals(True)
            self.ui.due_date_input.setDate(QDate(1970, 1, 1))
            self.ui.due_date_input.blockSignals(False)
        self.current_task_id = task_data['id']
        self.ui.task_title_2.setText(task_data['title'])
        self.ui.add_check.setChecked(task_data['important'])
        self.ui.done_check_3.setChecked(task_data['completed'])
        self.ui.input_note.setText(task_data['description'])
        self.ui.created_date_label.setText(f"Created on {task_data['created_date']}")

    def delete_task(self):
        """
        Delete the selected task from the database.
        """
        reply = QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.task_model.delete_task(self.current_task_id)
            QMessageBox.information(self, "Delete Task", "Task deleted!")
            self.load_all_tasks()

    def add_note(self):
        note_text = self.ui.input_note.text().strip()
        if note_text:
            self.task_model.update_task(self.current_task_id, description=note_text)
            QMessageBox.information(self,"Description", "Your Description has been saved!")
            self.load_all_tasks()

    def update_duedate(self, newdate):
        date_string = newdate.toString('dd/MM/yyyy')
        self.task_model.update_task(self.current_task_id, due_date=date_string)
        self.reload()

    def update_important(self):
        self.task_model.update_task(self.current_task_id, important=self.ui.add_check.isChecked())
        self.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainController()
    main_window.show()
    sys.exit(app.exec_())
