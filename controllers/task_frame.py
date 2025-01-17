from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal


class TaskFrame(QtWidgets.QFrame):
    """
    A reusable frame for tasks, supporting both completed and active tasks.
    - Includes done and important checkboxes.
    - Emits signals for updates and clicks.
    """

    # Define custom signals
    task_updated = pyqtSignal(dict)  # Signal emitted when the task is updated
    task_clicked = pyqtSignal(dict)  # Signal emitted when the task is clicked

    def __init__(self, task_id, task_model, completed=False, parent=None, is_highlight=False):
        super().__init__(parent)
        self.task_id = task_id
        self.task_model = task_model
        self.task_data = self.task_model.get_a_task(self.task_id)  # Fetch task data
        self.completed = completed  # Flag to differentiate between active and completed tasks
        self.is_highlight = is_highlight

        # Initialize frame styling
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.setMinimumHeight(60)
        if is_highlight:
            self.setStyleSheet("""
                QFrame {
                    border-radius: 5px;
                    background-color: rgb(243,243,243);
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    border-radius: 5px;
                    background-color: white;
                }
            """)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        # Create and set up the layout
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(-1, -1, -1, 9)

        # Create subcomponents
        self.task_name_frame = self._create_task_name_frame()
        self.important_frame = self._create_important_frame()

        # Add subcomponents to the layout
        self.main_layout.addWidget(self.task_name_frame, 0, QtCore.Qt.AlignLeft)
        self.main_layout.addWidget(self.important_frame, 0, QtCore.Qt.AlignRight)

    def _create_task_name_frame(self):
        """
        Create the frame containing the task title and done checkbox.
        """
        task_title = self.task_data["title"]
        task_done = self.task_data["completed"]

        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)

        layout = QtWidgets.QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

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
            QCheckBox {margin: 5px}
        """)
        self.done_check.setText("")
        self.done_check.setChecked(task_done)
        self.done_check.toggled.connect(self.update_done_status)

        # Task title label
        self.task_name_label = QtWidgets.QLabel(task_title)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(10)
        if self.completed:
            font.setStrikeOut(True)  # Strike through for completed tasks
        self.task_name_label.setFont(font)

        # Add components to the layout
        layout.addWidget(self.done_check)
        layout.addWidget(self.task_name_label)

        return frame

    def _create_important_frame(self):
        """
        Create the frame containing the important checkbox.
        """
        is_important = self.task_data["important"]

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

        # Add the checkbox to the layout
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
        Reload task data from the database and update the UI.
        """
        self.task_data = self.task_model.get_a_task(self.task_id)

    def update_done_status(self, checked):
        """
        Update the 'done' status in the database.
        """
        done_check = self.done_check.isChecked()
        self.task_model.update_task(self.task_id, completed=done_check)
        self.refresh_data()
        self.task_updated.emit(self.task_data)

    def update_important_status(self, checked):
        """
        Update the 'important' status in the database.
        """
        is_important = self.important_check.isChecked()
        self.task_model.update_task(self.task_id, important=is_important)
        self.refresh_data()
        self.task_updated.emit(self.task_data)

    def change_stylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)

