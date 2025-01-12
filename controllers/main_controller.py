import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.main_ui import Ui_MainWindow  # Import the generated UI class
from models.main_model import TaskModel  # Import the task model
from task_frame import TaskFrame  # Import the custom task frame
from done_task_frame import DoneTaskFrame


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

        # Load tasks into the UI
        self.load_tasks()

    def load_tasks(self):
        """
        Load tasks from the database and display them in the task list widget.
        """
        self.clear_layout(self.ui.verticalLayout_29)  # Clear the layout before adding new tasks
        self.clear_layout(self.ui.verticalLayout_30)  # Clear the layout before adding new tasks
        tasks = self.task_model.get_all_tasks()
        for task in tasks:
            task_id = task['id']
            if (task['completed'] == False):
                task_frame = TaskFrame(task_id, self.task_model)

                # Add task frame to the layout
                self.ui.verticalLayout_29.addWidget(task_frame)

                # Connect task frame signals to update task details
                task_frame.task_clicked.connect(self.update_task_details)
                task_frame.task_updated.connect(self.update_task_details)
                task_frame.task_updated.connect(self.reload)
            else:
                task_frame = DoneTaskFrame(task_id, self.task_model)
                self.ui.verticalLayout_30.addWidget(task_frame)
                task_frame.task_clicked.connect(self.update_task_details)
                task_frame.task_updated.connect(self.update_task_details)
                task_frame.task_updated.connect(self.reload)

    def reload(self):
        self.load_tasks()

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
        self.load_tasks()

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
        self.current_task_id = task_data['id']
        self.ui.task_title_2.setText(task_data['title'])
        self.ui.important_check_4.setChecked(task_data['important'])
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
            self.load_tasks()


    def add_note(self):
        note_text = self.ui.input_note.text().strip()
        if note_text:
            self.task_model.update_task(self.current_task_id, description=note_text)
            QMessageBox.information(self,"Description", "Your Description has been saved!")
            self.load_tasks()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainController()
    main_window.show()
    sys.exit(app.exec_())
