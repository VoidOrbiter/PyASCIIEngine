from PyQt6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout,
    QGridLayout, QLabel, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ProjectPanel(QWidget):
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
            card = QWidget()
            card_layout = QVBoxLayout(card)

            pixmap = QPixmap(proj.get("image", ""))
            img_label = QLabel()
            if not pixmap.isNull():
                img_label.setPixmap(pixmap.scaled(100, 100))
            else:
                img_label.setText("No Image")
                img_label.setFixedSize(100, 100)
                img_label.setStyleSheet("background-color: #444; color: #fff;")
                img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            name_label = QLabel(proj["name"])
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card_layout.addWidget(img_label)
            card_layout.addWidget(name_label)
            card.setMaximumWidth(120)
            card.setMaximumHeight(150)
            card.setObjectName("card")
            name_label.setObjectName("projectName")

            self.grid_layout.addWidget(card, row, col)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1