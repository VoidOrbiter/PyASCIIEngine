from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget
)
from PyQt6.QtCore import Qt

from src.pyascii_engine.ui.game_canvas import GameCanvas
from src.pyascii_engine.ui.right_sidebar import RightSidebar
from src.pyascii_engine.ui.left_sidebar import LeftSidebar
from src.pyascii_engine.pages.welcome_page import WelcomePage
from src.pyascii_engine.utils.editor_state import EditorState

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1920, 1080)
        self.setWindowTitle("Py ASCII Engine")

        self.state = EditorState.WELCOME

        # ------ STACKED WIDGET ------
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # ------ PAGES ------
        self.welcome_page   = WelcomePage(self)
        self.canvas         = GameCanvas()

        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.canvas)

        self.stack.setCurrentWidget(self.welcome_page)

        # ------ Project Path declaration ------
        project_path = self.welcome_page.get_project_path()

        # ------ RIGHT SIDEBAR ------
        self.right_sidebar = RightSidebar(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_sidebar)

        # ------ LEFT SIDEBAR ------
        self.left_sidebar = LeftSidebar([])
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_sidebar)

        self.update_ui_for_state()
        self.left_sidebar.project_selected.connect(self.load_project)

    def show_canvas(self):
        self.stack.setCurrentWidget(self.canvas)

    def update_ui_for_state(self):
        if self.state == EditorState.WELCOME:
            self.stack.setCurrentWidget(self.welcome_page)
            self.left_sidebar.hide()
            self.right_sidebar.hide()

        elif self.state == EditorState.EDITING:
            self.stack.setCurrentWidget(self.canvas)
            self.left_sidebar.show()
            self.right_sidebar.show()

        elif self.state == EditorState.PLAYTEST:
            self.stack.setCurrentWidget(self.canvas)
            self.left_sidebar.hide()
            self.right_sidebar.hide()

    def load_project(self, project_path):
        self.left_sidebar.set_project_path(project_path)

        self.state = EditorState.EDITING
        self.update_ui_for_state()

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    with open("resources/themes/main.qss", "r") as f:
        qss = f.read()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())