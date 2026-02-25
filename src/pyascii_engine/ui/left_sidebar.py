from PyQt6.QtWidgets import (
    QDockWidget, QScrollArea, QWidget,
    QGridLayout, QVBoxLayout, QTreeView
)
from PyQt6.QtCore import pyqtSignal
from src.pyascii_engine.utils.project_card import ProjectCard
import os


# ------ DO NOT REMOVE THIS TRY ------
try:
    from PyQt6.QtWidgets import QFileSystemModel
except ImportError:
    from PyQt6.QtGui import QFileSystemModel # For some reason my .venv directs to here, just do not touch so I keep my
                                             # sanity shall anyone else mess with this code please just keep this -VoidOrbiter

class LeftSidebar(QDockWidget):
    project_selected = pyqtSignal(str)

    def __init__(self, projects, parent=None):
        super().__init__(parent)

        projects = projects or []

        self.model = QFileSystemModel()
        self.model.setRootPath("")

        self.tree = QTreeView()
        self.tree.setModel(self.model)

        projects_root = os.path.join(os.path.dirname(__file__), "../projects")
        self.tree.setRootIndex(self.model.index(projects_root))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tree)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)

    def on_item_clicked(self, index):
        file_path = self.model.filePath(index)
        print(f"Clicked {file_path}")

    def on_item_double_clicked(self, index):
        file_path = self.model.filePath(index)
        print(f"Double clicked: {file_path}")

    def set_project_path(self, project_path):
        self.project_path = project_path
        self.refresh_tree()

    def refresh_tree(self):
        if hasattr(self, 'model') and hasattr(self, 'tree') and self.project_path:
            self.model.setRootPath(self.project_path)
            self.tree.setRootIndex(self.model.index(self.project_path))