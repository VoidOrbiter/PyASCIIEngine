from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox, QFileDialog
)

try:
    from PyQt6.QtWidgets import QFileSystemModel
except ImportError:
    from PyQt6.QtGui import QFileSystemModel
import os
import json

class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")
        self.setFixedWidth(400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Project Name:"))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("Project Folder:"))
        folder_layout = QHBoxLayout()
        self.folder_edit = QLineEdit()
        self.folder_button = QPushButton("...")
        self.folder_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(self.folder_button)
        layout.addLayout(folder_layout)

        layout.addWidget(QLabel("Initial Description(optional):"))
        self.desc_edit = QLineEdit()
        layout.addWidget(self.desc_edit)

        self.confirm_btn = QPushButton("Create Project")
        self.confirm_btn.clicked.connect(self.create_project)
        layout.addWidget(self.confirm_btn)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.folder_edit.setText(folder)

    def create_project(self):
        name = self.name_edit.text().strip()
        folder = self.folder_edit.text().strip()
        description = self.desc_edit.text().strip()

        if not name or not folder:
            QMessageBox.warning(self, "Error", "Project name and folder are required.")
            return

        project_path = os.path.join(folder, name)
        if os.path.exists(project_path):
            QMessageBox.warning(self, "Error", "Folder Already Exists")
            return

        os.makedirs(project_path)
        base_files = ["main.py", "objects.json", "scene.json"]
        for f in base_files:
            path = os.path.join(project_path, f)
            with open(path, "w", encoding="utf-8") as file:
                if f.endswith(".json"):
                    data = {"description": description} if f == "scene.json" else {}
                    json.dump(data, file, indent=2)

        os.makedirs(os.path.join(project_path, "assets"), exist_ok=True)

        QMessageBox.information(self, "Success", f"Project '{name}' created at {project_path}")
        self.accept()

    def get_project_name(self):
        return self.name_edit.text()

    def get_project_path(self):
        return self.folder_edit.text()