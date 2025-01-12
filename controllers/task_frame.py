from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal


class TaskFrame(QtWidgets.QFrame):
    """
    A custom QFrame representing a task. Each task includes:
    - A checkbox for marking it as done.
    - A label for the task title.
    - A checkbox for marking it as important.
    """

    # Define custom signals
    task_updated = pyqtSignal(dict)  # Signal emitted when the task is updated
    task_clicked = pyqtSignal(dict)  # Emitted when the task frame is clicked

    def __init__(self, task_id, task_model, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.task_model = task_model
        self.task_data = self.task_model.get_a_task(self.task_id)  # Store task data

        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.setMinimumHeight(60)
        self.setStyleSheet("""
            QFrame {
                border-radius: 5px;
                background-color: white;
            }
        """)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        # Main layout for the task frame
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(-1, -1, -1, 9)

        # Task name and done checkbox
        self.task_name_frame = self._create_task_name_frame()

        # Important checkbox
        self.important_frame = self._create_important_frame()

        # Add subframes to the main layout
        self.main_layout.addWidget(self.task_name_frame, 0, QtCore.Qt.AlignLeft)
        self.main_layout.addWidget(self.important_frame, 0, QtCore.Qt.AlignRight)

    def _create_task_name_frame(self):
        """
        Create the frame containing the task title and done checkbox.
        """
        task_title = self.task_data['title']
        task_done = self.task_data['completed']
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)

        layout = QtWidgets.QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Done checkbox
        self.done_check = QtWidgets.QCheckBox()
        self.done_check.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.done_check.setStyleSheet("""
            QCheckBox::indicator::unchecked {
                image: url(:/icon/icons/circle.png); 
                height: 20px; 
                width: 20px;
            }
            QCheckBox::indicator::checked {
                image: url(:/icon/icons/check_fill.png); 
                height: 20px; 
                width: 20px;
            }
        """)
        self.done_check.setText("")
        self.done_check.setChecked(task_done)
        self.done_check.toggled.connect(self.update_done_status)

        # Task title label
        self.task_name_label = QtWidgets.QLabel(task_title)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(10)
        self.task_name_label.setFont(font)

        # Add checkbox and label to the layout
        layout.addWidget(self.done_check)
        layout.addWidget(self.task_name_label)

        return frame

    def _create_important_frame(self):
        """
        Create the frame containing the important checkbox.
        """
        is_important = self.task_data['important']
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)

        layout = QtWidgets.QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Important checkbox
        self.important_check = QtWidgets.QCheckBox()
        self.important_check.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.important_check.setFont(font)
        self.important_check.setStyleSheet("""
            QCheckBox::indicator::unchecked {
                image: url(:/icon/icons/star.png); 
                height: 25px; 
                width: 25px;
            }
            QCheckBox::indicator::checked {
                image: url(:/icon/icons/star_fill.png); 
                height: 25px; 
                width: 25px;
            }
        """)
        self.important_check.setText("")
        self.important_check.setChecked(is_important)
        self.important_check.toggled.connect(self.update_important_status)

        # Add checkbox to the layout
        layout.addWidget(self.important_check)

        return frame

    def mousePressEvent(self, event):
        """
        Emit signal when the frame is clicked.
        """

        self.refresh_data()
        self.task_clicked.emit(self.task_data)
        super().mousePressEvent(event)

    def refresh_data(self):
        """
        Load task details from the database and update the UI.
        """
        self.task_data = self.task_model.get_a_task(self.task_id)

    def update_done_status(self, checked):
        """
        Update the "done" status of the task in the database.
        """
        done_check = self.done_check.isChecked()
        self.task_model.update_task(self.task_id, completed=done_check)
        self.refresh_data()
        self.task_updated.emit(self.task_data)  # Emit signal to notify other components

    def update_important_status(self, checked):
        """
        Update the "important" status of the task in the database.
        """
        is_important = self.important_check.isChecked()
        self.task_model.update_task(self.task_id, important=is_important)
        self.refresh_data()
        self.task_updated.emit(self.task_data)  # Emit signal to notify other components