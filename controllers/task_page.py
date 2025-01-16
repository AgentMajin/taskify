from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QScrollArea
from task_frame import TaskFrame
from datetime import datetime, date, timedelta

today = date.today()
# today = (date.today() + timedelta(days=1))
today_str = today.strftime("%d/%m/%Y")
tomorrow_str = (today + timedelta(days=1)).strftime('%d/%m/%Y')

class TaskPage(QWidget):
    def __init__(self, data_model, bg_url: str,
                 title: str,
                 important_only: bool = False,
                 overdued_only: bool = False,
                 show_completed: bool = True,
                 allow_adding_task: bool = True,
<<<<<<< HEAD
                 myday: bool = False,):
=======
                 myday: bool = False):
>>>>>>> fe505797a552cbb4da9b0c4220fa43164c53313e
        self.data_model = data_model
        self.bg_url = bg_url
        self.title = title
        self.show_completed = show_completed
        self.allow_adding_task = allow_adding_task
        self.overdued_only = overdued_only
        self.important_only = important_only
        self.myday = myday
        self.task_clicked_callback = None
        self.task_updated_callback = None

        super().__init__()
        self.setup_ui()


        if allow_adding_task:
            self.add_task_button.clicked.connect(self.add_task)
        if show_completed:
            self.show_completed_4.clicked.connect(self.show_hide_completed)
        else:
            self.show_completed_4.hide()
    def setup_ui(self):
        """
        Initialize the UI components for the Task Page.
        """
        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)



        self.setObjectName("Task Page")
        self.verticalLayout_page = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_page.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_page.setSpacing(0)
        self.verticalLayout_page.setObjectName("verticalLayout_page")
        self.Task = QtWidgets.QFrame(self)
        self.Task.setStyleSheet("#Task {\n"
                                "    margin: 0px;\n"
                                f"    background-image: {self.bg_url};\n"
                                "    background-position: center;\n"
                                "    background-repeat: no-repeat;\n"
                                "    border-radius: 10px;\n"
                                "    background-size: 100% 100%;\n"
                                "}")
        self.Task.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Task.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Task.setObjectName("Task")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.Task)
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_26.setSpacing(0)
        self.verticalLayout_26.setObjectName("verticalLayout_26")

        self.task_title_frame_5 = QtWidgets.QFrame(self.Task)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.task_title_frame_5.sizePolicy().hasHeightForWidth())
        self.task_title_frame_5.setSizePolicy(sizePolicy)
        self.task_title_frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.task_title_frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.task_title_frame_5.setObjectName("task_title_frame_5")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.task_title_frame_5)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(20,20,0,0)
        self.task_title_5 = QtWidgets.QLabel(self.task_title_frame_5)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.task_title_5.setFont(font)
        self.task_title_5.setStyleSheet("color: white")
        self.task_title_5.setObjectName("task_title_5")
        self.verticalLayout_28.addWidget(self.task_title_5)
        self.verticalLayout_26.addWidget(self.task_title_frame_5)

        # Scroll Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background:transparent")

        self.content_frame_4 = QtWidgets.QFrame(self.Task)
        self.content_frame_4.setStyleSheet("")
        self.content_frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content_frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content_frame_4.setObjectName("content_frame_4")
        self.horizontalLayout_52 = QtWidgets.QHBoxLayout(self.content_frame_4)
        self.horizontalLayout_52.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_52.setObjectName("horizontalLayout_52")
        self.task_view_4 = QtWidgets.QFrame(self.content_frame_4)
        self.task_view_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.task_view_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.task_view_4.setObjectName("task_view_4")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout(self.task_view_4)
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_27.setSpacing(0)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.task_to_do_4 = QtWidgets.QFrame(self.task_view_4)
        self.task_to_do_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.task_to_do_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.task_to_do_4.setObjectName("task_to_do_4")
        self.verticalLayout_task_to_do = QtWidgets.QVBoxLayout(self.task_to_do_4)
        self.verticalLayout_task_to_do.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_task_to_do.setSpacing(4)
        self.verticalLayout_task_to_do.setObjectName("verticalLayout_task_to_do")
        self.verticalLayout_27.addWidget(self.task_to_do_4, 0, QtCore.Qt.AlignTop)
        self.show_completed_4 = QtWidgets.QPushButton(self.task_view_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_completed_4.sizePolicy().hasHeightForWidth())
        self.show_completed_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(10)
        self.show_completed_4.setFont(font)
        self.show_completed_4.setStyleSheet("border-radius: 5px;      /* Rounded corners */\n"
                                            "    background-color: rgb(237,204,204);"
                                            "padding: 8px")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icon/keyboard-down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_completed_4.setIcon(icon7)
        self.show_completed_4.setObjectName("show_completed_4")
        self.verticalLayout_27.addWidget(self.show_completed_4)
        self.task_completed_4 = QtWidgets.QFrame(self.task_view_4)
        self.task_completed_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.task_completed_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.task_completed_4.setObjectName("task_completed_4")
        if self.show_completed:
            self.verticalLayout_done_task = QtWidgets.QVBoxLayout(self.task_completed_4)
            self.verticalLayout_done_task.setContentsMargins(0, -1, 0, 0)
            self.verticalLayout_done_task.setSpacing(4)
            self.verticalLayout_done_task.setObjectName("verticalLayout_done_task")
        self.verticalLayout_27.addWidget(self.task_completed_4, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_52.addWidget(self.task_view_4, 0, QtCore.Qt.AlignTop)

        self.scroll_area.setWidget(self.content_frame_4)
        self.verticalLayout_26.addWidget(self.scroll_area)
        if self.allow_adding_task:
            self.add_task_frame_7 = QtWidgets.QFrame(self.Task)
            self.add_task_frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.add_task_frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
            self.add_task_frame_7.setObjectName("add_task_frame_7")
            self.verticalLayout_31 = QtWidgets.QVBoxLayout(self.add_task_frame_7)
            self.verticalLayout_31.setObjectName("verticalLayout_31")
            self.add_task_frame_8 = QtWidgets.QFrame(self.add_task_frame_7)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.add_task_frame_8.sizePolicy().hasHeightForWidth())
            self.add_task_frame_8.setSizePolicy(sizePolicy)
            self.add_task_frame_8.setStyleSheet("QFrame #add_task_frame_8 {\n"
                                                "     /* Solid black border */\n"
                                                "    border-radius: 5px;      /* Rounded corners */\n"
                                                "    background-color: white\n"
                                                "}")
            self.add_task_frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.add_task_frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
            self.add_task_frame_8.setObjectName("add_task_frame_8")
            self.horizontalLayout_63 = QtWidgets.QHBoxLayout(self.add_task_frame_8)
            self.horizontalLayout_63.setContentsMargins(-1, -1, -1, 9)
            self.horizontalLayout_63.setObjectName("horizontalLayout_63")
            self.add_button_frame_4 = QtWidgets.QFrame(self.add_task_frame_8)
            self.add_button_frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.add_button_frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
            self.add_button_frame_4.setObjectName("add_button_frame_4")
            self.horizontalLayout_64 = QtWidgets.QHBoxLayout(self.add_button_frame_4)
            self.horizontalLayout_64.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_64.setSpacing(0)
            self.horizontalLayout_64.setObjectName("horizontalLayout_64")
            self.add_task_button = QtWidgets.QPushButton(self.add_button_frame_4)
            self.add_task_button.setStyleSheet("border:none")
            self.add_task_button.setText("")
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap(":/icon/icons/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.add_task_button.setIcon(icon8)
            self.add_task_button.setObjectName("add_task_button")
            self.horizontalLayout_64.addWidget(self.add_task_button)
            self.horizontalLayout_63.addWidget(self.add_button_frame_4, 0, QtCore.Qt.AlignLeft)
            self.task_input_4 = QtWidgets.QLineEdit(self.add_task_frame_8)
            font = QtGui.QFont()
            font.setFamily("Microsoft JhengHei")
            font.setPointSize(10)
            self.task_input_4.setFont(font)
            self.task_input_4.setStyleSheet("border: none")
            self.task_input_4.setObjectName("task_input_4")
            self.horizontalLayout_63.addWidget(self.task_input_4)
            self.verticalLayout_31.addWidget(self.add_task_frame_8)
            self.verticalLayout_26.addWidget(self.add_task_frame_7, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout_page.addWidget(self.Task)
        # self.scroll_area.setWidget(self.Task)
        self.main_layout.addWidget(self.Task)
        self.show_completed_4.setText( "Hide Completed")
        self.task_title_5.setText(f"{self.title}")

    def add_task(self):
        task_title = self.task_input_4.text().strip()
        if not task_title:
            QMessageBox.warning(self, "Error", "Task title cannot be empty!")
            return

        # Add the task to the database
        if self.important_only:
            self.data_model.add_task(task_title, important=True)
        elif self.myday:
            self.data_model.add_task(task_title, is_myday=True, expired_date_myday=tomorrow_str)
        else:
            self.data_model.add_task(task_title)

        # Clear the input field
        self.task_input_4.clear()

    def filter_task(self):
<<<<<<< HEAD
=======


>>>>>>> fe505797a552cbb4da9b0c4220fa43164c53313e
        filtered_tasks = self.data_model.get_all_tasks()

        # Filter important tasks
        if self.important_only:
            # filtered_tasks = [task for task in tasks if task.get("important", False)]
            filtered_tasks = self.data_model.get_task_condition(important=True)
        # Filter overdue tasks
        if self.overdued_only:
            filtered_tasks = []
            incompleted_task = self.data_model.get_task_condition(completed=False)
            for task in incompleted_task:
                due_date_str = task.get('due_date') or '01/01/1970'  # Use default if due_date is None or empty
                due_date = datetime.strptime(due_date_str, "%d/%m/%Y").date()
<<<<<<< HEAD
                if due_date < today and due_date != datetime.strptime('01/01/1970', '%d/%m/%Y').date():
=======
                if due_date < today:
>>>>>>> fe505797a552cbb4da9b0c4220fa43164c53313e
                    filtered_tasks.append(task)

        # Filter myday Tasks
        if self.myday:
            myday_tasks = self.data_model.get_task_condition(is_myday=True, expired_date_myday=tomorrow_str)
            due_today = self.data_model.get_task_condition(due_date=today_str, is_myday=False)
            filtered_tasks = myday_tasks + due_today

        return filtered_tasks

<<<<<<< HEAD
    def filter_search_keyword(self, search_keyword, tasks):
        if search_keyword is not None:
            search_keyword = search_keyword.lower()
            filtered_tasks = [task for task in tasks if (search_keyword in task.get('title').lower())]
            return filtered_tasks
        return tasks

    def reload_task(self, task_clicked_callback: list,
                    task_updated_callback: list,
                    detail_task_id=None,
                    search_keyword=None):
=======

    def reload_task(self, task_clicked_callback, task_updated_callback):
>>>>>>> fe505797a552cbb4da9b0c4220fa43164c53313e
        """
        Reload tasks into the given layout.
        """
        # Save callback function for buttons to assign when loading task again in hide_completed method
        if task_clicked_callback:
            self.task_clicked_callback = task_clicked_callback
        if task_updated_callback:
            self.task_updated_callback = task_updated_callback
<<<<<<< HEAD
        if detail_task_id:
            self.detail_task_id = detail_task_id
        if search_keyword:
            self.search_keyword = search_keyword
=======
>>>>>>> fe505797a552cbb4da9b0c4220fa43164c53313e

        # Determine which layout to load task into: to do layout only or both to do layout and done task layout
        layouts = [self.verticalLayout_task_to_do]
        if self.show_completed:
            layouts = [self.verticalLayout_task_to_do, self.verticalLayout_done_task]

        # Clear tasks from layouts
        for layout in layouts:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        # Filter which tasks to show using class arguments
        # tasks = self.data_model.get_all_tasks()
        tasks = self.filter_task()
<<<<<<< HEAD
        if tasks:
            tasks = self.filter_search_keyword(search_keyword, tasks)
=======
>>>>>>> fe505797a552cbb4da9b0c4220fa43164c53313e

        # Load tasks into layouts and assign callback function
        for task in tasks:
            if task["completed"] == True and self.show_completed == True:
                layout = self.verticalLayout_done_task
<<<<<<< HEAD
            elif not task["completed"]:
                layout = self.verticalLayout_task_to_do
            else:
                continue
            if detail_task_id is None or detail_task_id != task['id']:
                task_frame = TaskFrame(task["id"], self.data_model, completed=task["completed"])
            else:
                task_frame = TaskFrame(task["id"], self.data_model, completed=task["completed"], is_highlight=True)
            layout.addWidget(task_frame)

            for callback in task_clicked_callback:
                task_frame.task_clicked.connect(callback)
            for callbacks in task_updated_callback:
                task_frame.task_updated.connect(callbacks)
=======
            elif task["completed"] == False:
                layout = self.verticalLayout_task_to_do
            else:
                continue
            task_frame = TaskFrame(task["id"], self.data_model, completed=task["completed"])
            layout.addWidget(task_frame)
            task_frame.task_clicked.connect(task_clicked_callback)
            for callback in task_updated_callback:
                task_frame.task_updated.connect(callback)
>>>>>>> fe505797a552cbb4da9b0c4220fa43164c53313e

        # Change text of show/hide button to Hide Completed (since after reload, done task layout automatically show)
        self.show_completed_4.setText("Hide Completed")

    def show_hide_completed(self):
        if self.show_completed_4.text() == "Hide Completed":
            while self.verticalLayout_done_task.count():
                item = self.verticalLayout_done_task.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.show_completed_4.setText("Show Completed")
        else:
<<<<<<< HEAD
            self.reload_task(self.task_clicked_callback,
                             self.task_updated_callback,
                             self.detail_task_id,
                             self.search_keyword)
=======
            self.reload_task(self.task_clicked_callback, self.task_updated_callback)
>>>>>>> fe505797a552cbb4da9b0c4220fa43164c53313e
            self.show_completed_4.setText("Hide Completed")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    page = TaskPage()
    page.setup_ui()
    window = QtWidgets.QMainWindow()
    window.setCentralWidget(page)
    window.show()
    sys.exit(app.exec_())
