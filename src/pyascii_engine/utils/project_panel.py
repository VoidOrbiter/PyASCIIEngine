from PyQt6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout,
    QGridLayout, QLabel, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from src.pyascii_engine.utils.project_card import ProjectCard

class ProjectPanel(QWidget):
    project_selected = pyqtSignal(str)
    def __init__(self, projects):
        super().__init__()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setSpacing(10)
        scroll.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        self.populate_grid(projects)

    def populate_grid(self, projects):
        max_columns = 4
        row = 0
        col = 0

        for proj in projects:
            card = ProjectCard(proj)
            card.clicked.connect(self.project_selected.emit)
            self.grid_layout.addWidget(card, row, col)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1
