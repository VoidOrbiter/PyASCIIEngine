from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import pyqtSignal
import uuid
import json
import os

class NewObjectDialog(QDialog):
    object_created = pyqtSignal(dict)

    def __init__(self, default_folder=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create a New Object")
        self.setFixedWidth(400)
        self.default_folder = default_folder

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Object Name:"))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("Object Character (1 Char):"))
        self.char_edit = QLineEdit()
        layout.addWidget(self.char_edit)

        layout.addWidget(QLabel("Description:"))
        self.desc_edit = QLineEdit()
        layout.addWidget(self.desc_edit)

        layout.addWidget(QLabel("Object Type (For Categorization):"))
        self.type_edit = QLineEdit()
        layout.addWidget(self.type_edit)

        self.confirm_btn = QPushButton("Create Object")
        self.confirm_btn.clicked.connect(self.create_object)
        layout.addWidget(self.confirm_btn)

    def create_object(self):
        name = self.name_edit.text().strip()
        char = self.char_edit.text().strip()
        desc = self.desc_edit.text().strip()
        obj_type = self.type_edit.text().strip() or "default"

        if not name or not char:
            QMessageBox.warning(self, "Error", "Object name and character are required.")
            return

        obj = {
            "id": str(uuid.uuid4()),
            "name": name,
            "symbol": char,
            "description": desc,
            "instance_type": obj_type
        }

        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder to Save Object", self.default_folder or os.getcwd()
        )

        if folder:
            file_path = os.path.join(folder, f"{name}.json")
            if os.path.exists(file_path):
                QMessageBox.warning(self, "Error", "A file with this name already exists.")
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(obj, f, indent=2)

        self.object_created.emit(obj)
        self.accept()