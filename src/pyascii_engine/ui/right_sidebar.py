from PyQt6.QtWidgets import (
    QDockWidget, QVBoxLayout, QLabel,
    QListWidgetItem,
    QPushButton, QWidget, QInputDialog
)
from PyQt6.QtCore import Qt
import uuid
from src.pyascii_engine.utils.draggable_list_widget import DraggableListWidget

class RightSidebar(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Objects")
        self.setFixedWidth(200)

        # ------ CONTAINER ------
        container   = QWidget()
        layout      = QVBoxLayout()
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

    def add_new_object(self):
        name, ok = QInputDialog.getText(self, "Object name", "Enter Object name:")
        if not ok or not name:
            return

        symbol, ok = QInputDialog.getText(self, "Object Symbol", "Enter symbol (1 char):")
        if not ok or not symbol:
            return

        description, ok = QInputDialog.getText(self, "Description", "Enter Description:")
        if not ok:
            description = ""

        instance_type, ok = QInputDialog.getText(self, "Instance Type", "Enter Instance Type:")
        if not ok or not instance_type:
            instance_type = "default"

        obj = {
            "id": str(uuid.uuid4()),
            "name": name,
            "symbol": symbol,
            "description": description,
            "instance_type": instance_type
        }

        self.add_object(obj)

    def add_object(self, obj):
        item = QListWidgetItem(f"{obj['name']} ({obj['id'][:8]})")
        item.setData(Qt.ItemDataRole.UserRole, obj)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsDragEnabled)
        self.list_widget.addItem(item)