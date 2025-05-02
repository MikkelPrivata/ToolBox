import os
import sys
from PySide6 import QtWidgets as Widgets, QtGui as GUI
from PySide6.QtWidgets import QTextEdit as TextEdit, QMenuBar as MenuBar, QStatusBar as StatusBar
from PySide6.QtGui import QAction as Action

short_message_duration = 2000 # milliseconds
toolbox_name = "TOOLBOX"
text_editor_name = "Texty"
word_processor_name = "Wordy"
toolbox_text_editor_title = toolbox_name + " | " + text_editor_name
toolbox_word_processor_title = toolbox_name + " | " + word_processor_name

class MainWindow(Widgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.document_modified = False
        self.file_path = None

        #--------------------------------------------------------------
        #> WINDOW
        self.set_window_title(toolbox_text_editor_title)
        #self.setGeometry(100, 100, 800, 600)
        #self.showFullScreen()
        screen_geometry = Widgets.QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.resize(screen_width, screen_height)

        #--------------------------------------------------------------
        #> MENU BAR
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("File")

        new_action = Action("New", self);           new_action.setShortcut(GUI.QKeySequence("Ctrl+N"))
        open_action = Action("Open", self);         open_action.setShortcut(GUI.QKeySequence("Ctrl+O"))
        save_action = Action("Save", self);         save_action.setShortcut(GUI.QKeySequence("Ctrl+S"))
        save_as_action = Action("Save As", self);   save_as_action.setShortcut(GUI.QKeySequence("Ctrl+Shift+S"))
        
        file_menu.addAction(new_action);    new_action.triggered.connect(self.new_file)
        file_menu.addAction(open_action);   open_action.triggered.connect(self.open_file)
        file_menu.addAction(save_action);   save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_as_action);save_as_action.triggered.connect(self.save_file_as)

        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        #--------------------------------------------------------------
        #> TOOLBAR


        #--------------------------------------------------------------
        #> TEXT EDIT FIELD
        self.text_document_name = "Untitled"
        self.set_window_title(toolbox_text_editor_title + " - " + self.text_document_name)

        self.text_edit_field = TextEdit(self)
        self.text_edit_field.setGeometry(50, 50, 700, 500)

        font = GUI.QFont("Courier New", 12)
        self.text_edit_field.setFont(font)

        self.text_edit_field.textChanged.connect(self.on_text_changed)

        self.setCentralWidget(self.text_edit_field)

    def set_window_title(self, title):
        self.setWindowTitle(title)

    def on_text_changed(self):
        if not self.document_modified:
            self.document_modified = True
            self.update_window_title()
    
    def update_window_title(self):
        modified_indicator = "*" if self.document_modified else ""
        self.set_window_title(toolbox_text_editor_title + " - " + self.text_document_name + " " + modified_indicator)

    def new_file(self):
        self.text_edit_field.clear()
        self.document_modified = False

        self.text_document_name = "Untitled"
        self.set_window_title(toolbox_text_editor_title + " - " + self.text_document_name)

        self.status_bar.showMessage("New file created", short_message_duration)

    def open_file(self):
        file_path, selected_filter = Widgets.QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        self.file_path = file_path

        if file_path: # Check if a file was selected
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_edit_field.setPlainText(content)
                self.status_bar.showMessage(f"Opened file: {file_path}", short_message_duration)

                self.text_document_name = os.path.basename(file_path)
                self.set_window_title(toolbox_text_editor_title + " - " + self.text_document_name)

                self.document_modified = False
    
    def save_file(self):
        if not self.file_path:
            file_path, selected_filter = Widgets.QFileDialog.getSaveFileName(self, "Save as", self.text_document_name, "Text Files (*.txt);;All Files (*)")
            self.file_path = file_path
        self.write_file(self.file_path)

    def save_file_as(self):
        file_path, selected_filter = Widgets.QFileDialog.getSaveFileName(self, "Save as", self.text_document_name, "Text Files (*.txt);;All Files (*)")
        self.file_path = file_path
        self.write_file(self.file_path)

    def write_file(self, file_path):
        with open(file_path, 'w') as file:
            content = self.text_edit_field.toPlainText()
            file.write(content)
            self.status_bar.showMessage(f"Saved as: {file_path}", short_message_duration)

            self.text_document_name = os.path.basename(file_path)
            self.set_window_title(toolbox_text_editor_title + " - " + self.text_document_name)

            self.document_modified = False


if __name__ == "__main__":
    app = Widgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())