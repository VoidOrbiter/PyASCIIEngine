from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (
    QPainter, QColor, QDragEnterEvent,
    QDropEvent
)
from PyQt6.QtCore import Qt, QRect

class GameCanvas(QWidget):
    def __init__(self, grid_size=32, parent=None):
        super().__init__(parent)
        self.grid_size = grid_size
        self.setAcceptDrops(True)
        self.objects = []

        self.dragging_obj = None
        self.drag_offset = (0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        for x in range(0, self.width(), self.grid_size):
            painter.setPen(QColor(60, 60, 60))
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), self.grid_size):
            painter.setPen(QColor(60, 60, 60))
            painter.drawLine(0, y, self.width(), y)

        for obj in self.objects:
            rect_x = obj['x']
            rect_y = obj['y']
            painter.fillRect(rect_x, rect_y, self.grid_size, self.grid_size, QColor(200, 100, 100))
            painter.drawText(rect_x, rect_y, self.grid_size, self.grid_size, Qt.AlignmentFlag.AlignCenter, obj['name'])

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        pos     = event.position()
        x       = int(pos.x() // self.grid_size) * self.grid_size
        y       = int(pos.y() // self.grid_size) * self.grid_size

        obj_name = event.mimeData().text()
        self.objects.append({'name': obj_name, 'x': x, 'y': y})
        self.update()
        event.acceptProposedAction()

    def mousePressEvent(self, event):
        for obj in reversed(self.objects):
            rect = QRect(obj['x'], obj['y'], self.grid_size, self.grid_size)
            if rect.contains(event.position().toPoint()):
                self.dragging_obj = obj
                break

    def mouseMoveEvent(self, event):
        if self.dragging_obj and event.buttons() & Qt.MouseButton.LeftButton:
            self.dragging_obj['x'] = int(event.position().x() // self.grid_size) * self.grid_size
            self.dragging_obj['y'] = int(event.position().y() // self.grid_size) * self.grid_size
            self.update()

    def mouseReleaseEvent(self, event):
        if self.dragging_obj:
            self.dragging_obj = None

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GameCanvas()
    window.show()
    sys.exit(app.exec())