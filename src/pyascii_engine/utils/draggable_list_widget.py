from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag

class DraggableListWidget(QListWidget):
    def mouseMoveEvent(self, event):
        item = self.currentItem()
        if not item:
            return

        if event.buttons() & Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()

            mime.setText(item.text())
            obj = item.data(Qt.ItemDataRole.UserRole)
            mime.setData("application/x-obj", obj['symbol'].encode('utf-8'))
            drag.setMimeData(mime)
            drag.exec(Qt.DropAction.MoveAction)