from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QHBoxLayout, QTextEdit,
    QPushButton, QMessageBox
)
import os, json
from src.pyascii_engine.utils.project_dialog import NewProjectDialog
from src.pyascii_engine.utils.project_panel import ProjectPanel

class WelcomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Welcome To PyASCIIEngine")
        self.main_window = main_window
        # ------ Layouts ------
        self.main_layout = QVBoxLayout()
        self.main_panel  = QHBoxLayout()

        # ------ TOP UPDATE PANEL ------
        self.updates_panel = QTextEdit()
        self.updates_panel.setReadOnly(True)
        self.updates_panel.setPlainText(
            "EARLY VERSION TEXT FOR TESTING\n"
            "YEH BRUH"
                                        )
        self.updates_panel.setMaximumHeight(150)

        self.updates_panel.setSizePolicy(
            self.updates_panel.sizePolicy().horizontalPolicy(),
            self.updates_panel.sizePolicy().verticalPolicy()
        )

        # ------ PROJECT GRID PANEL ------
        self.projects_root = os.path.join(os.path.dirname(__file__), "../projects")
        os.makedirs(self.projects_root, exist_ok=True)
        self.projects_file = os.path.join(self.projects_root, "projects.json")
        if not os.path.exists(self.projects_file):
            with open(self.projects_file, "w") as f:
                json.dump([], f)

        with open(self.projects_file, "r") as f:
            self.projects_data = json.load(f)

        self.projects_panel = ProjectPanel(self.projects_data)
        self.main_panel.addWidget(self.projects_panel)

        # ------ PROJECT BUILDING ------
        self.new_project_btn = QPushButton("New Project")
        self.new_project_btn.clicked.connect(self.create_new_project)
        self.main_panel.addWidget(self.new_project_btn)
        # ------ APPLYING TO THE MAIN LAYOUT ------
        self.main_layout.addWidget(self.updates_panel)
        self.main_layout.addLayout(self.main_panel)
        self.setLayout(self.main_layout)

        self.current_project_path = None
        self.projects_panel.project_selected.connect(self.load_project)

    def create_new_project(self):
        dialog = NewProjectDialog()
        if dialog.exec():
            project_path = dialog.get_full_path()
            project_name = dialog.get_project_name()

            if not project_name:
                return

            if not os.path.exists(project_path):
                QMessageBox.warning(self, "Error", "Project folder not found.")
                return

        if self.main_window and hasattr(self.main_window, "left_sidebar"):
            self.main_window.left_sidebar.set_project_path(os.path.dirname(project_path))

            engine_root = os.path.dirname(os.path.dirname(__file__))
            projects_root = os.path.join(engine_root, "projects")
            os.makedirs(projects_root, exist_ok=True)

            project_path = os.path.join(projects_root, project_name)
            if os.path.exists(project_path):
                QMessageBox.warning(self, "Error", f"Project '{project_name}' already exists.")
                return
            os.makedirs(project_path)

            self.current_project_path = project_path

            projects_file = os.path.join(projects_root, "projects.json")
            if not os.path.exists(projects_file):
                with open(projects_file, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)

            with open(projects_file, "r", encoding="utf-8") as f:
                projects = json.load(f)

            projects.append({
                "name": project_name,
                "path": project_path,
                "image": ""
            })

            with open(projects_file, "w", encoding="utf-8") as f:
                json.dump(projects, f, indent=4)

            # create base files
            base_files = ["main.py", "objects.json", "scene.json"]
            for f in base_files:
                path = os.path.join(project_path, f)
                with open(path, "w", encoding="utf-8") as file:
                    if f.endswith(".json"):
                        json.dump({}, file, indent=2)

            os.makedirs(os.path.join(project_path, "assets"), exist_ok=True)

            QMessageBox.information(self, "Success", f"Project '{project_name}' created at {project_path}")

            self.projects_panel.populate_grid(projects)
            self.main_window.left_sidebar.populate_grid(projects)

            self.current_project_path = project_path
            self.load_project(self.current_project_path)


    def get_project_path(self):
        return self.current_project_path

    def load_project(self, path):
        self.current_project_path = path
        if self.main_window:
            self.main_window.load_project(path)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = WelcomePage()
    window.show()
    app.exec()
