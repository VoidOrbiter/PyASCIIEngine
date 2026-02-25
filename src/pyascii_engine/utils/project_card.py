from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QMouseEvent

class ProjectCard(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, project):
        super().__init__()
        self.project_path = project["path"]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        pixmap      = QPixmap(project.get("image", ""))
        img_label   = QLabel()
        if not pixmap.isNull():
            img_label.setPixmap(pixmap.scaled(100, 100))
        else:
            img_label.setText("No Image")
            img_label.setFixedSize(100, 100)
            img_label.setStyleSheet("background-color: #444; color: #fff;")
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name_label = QLabel(project["name"])
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(img_label)
        layout.addWidget(name_label)
        self.setLayout(layout)
        self.setMaximumWidth(120)
        self.setMaximumHeight(150)
        self.setStyleSheet("border: 1px solid #555; border-radius: 4px;")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.project_path)