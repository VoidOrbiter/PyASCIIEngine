from PyQt6.QtWidgets import (
    QDockWidget, QTreeView, QWidget,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import Qt, QDir

# ------ DO NOT REMOVE THIS TRY ------
try:
    from PyQt6.QtWidgets import QFileSystemModel
except ImportError:
    from PyQt6.QtGui import QFileSystemModel # For some reason my .venv directs to here, just do not touch so I keep my
                                             # sanity shall anyone else mess with this code please just keep this -VoidOrbiter

class LeftSidebar(QDockWidget):
    def __init__(self, project_root: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Project Explorer")
        self.setFixedWidth(250)

        # ------ CONTAINER FOR THE LAYOUT ------
        container   = QWidget()
        layout      = QVBoxLayout()
        container.setLayout(layout)

        layout.addWidget(QLabel("Project Files:"))

        self.model = QFileSystemModel()
        self.model.setRootPath(project_root)
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(project_root))
        self.tree.setHeaderHidden(True)
        self.tree.setSortingEnabled(True)

        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDragDropMode(QTreeView.DragDropMode.DragOnly)

        layout.addWidget(self.tree)
        self.setWidget(container)

        self.tree.clicked.connect(self.on_item_clicked)
        self.tree.doubleClicked.connect(self.on_item_double_clicked)

    def on_item_clicked(self, index):
        file_path = self.model.filePath(index)
        print(f"Clicked {file_path}")

    def on_item_double_clicked(self, index):
        file_path = self.model.filePath(index)
        print(f"Double clicked: {file_path}")