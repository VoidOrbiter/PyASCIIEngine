from PyQt6.QtWidgets import (
    QDockWidget, QVBoxLayout, QLabel,
    QListWidgetItem,
    QPushButton, QWidget
)
from PyQt6.QtCore import Qt
from src.pyascii_engine.utils.new_object_dialog import NewObjectDialog
from src.pyascii_engine.utils.draggable_list_widget import DraggableListWidget


class RightSidebar(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Objects")
        self.setFixedWidth(200)

        # ------ CONTAINER ------
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        # ------ LIST OF THE OBJECTS ------
        layout.addWidget(QLabel("Objects in the scene:"))
        self.list_widget = DraggableListWidget()
        layout.addWidget(self.list_widget)

        # ------ BUTTON THAT ADDS NEW OBJECT ------
        self.add_button = QPushButton("Add new object")
        self.add_button.clicked.connect(self.add_new_object)
        layout.addWidget(self.add_button)

        self.setWidget(container)

    def set_project_path(self, path):
        self.project_path = path

    def add_new_object(self):
        dialog = NewObjectDialog(default_folder=self.project_path)
        dialog.object_created.connect(self.add_object)
        dialog.exec()

    def add_object(self, obj):
        item = QListWidgetItem(f"{obj['name']} ({obj['id'][:8]})")
        item.setData(Qt.ItemDataRole.UserRole, obj)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsDragEnabled)
        self.list_widget.addItem(item)