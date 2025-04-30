import sys
from PySide6 import QtWidgets as Widgets
from PySide6.QtWidgets import QTextEdit as TextEdit, QMenuBar as MenuBar, QStatusBar as StatusBar
from PySide6.QtGui import QAction as Action

class MainWindow(Widgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #--------------------------------------------------------------
        #> WINDOW
        self.setWindowTitle("ToolBox")
        self.setGeometry(100, 100, 800, 600)

        #--------------------------------------------------------------
        #> MENU BAR
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("File")

        new_action = Action("New", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        #--------------------------------------------------------------
        #> TEXT EDIT FIELD
        self.text_edit = TextEdit(self)
        self.text_edit.setGeometry(50, 50, 700, 500)

        self.setCentralWidget(self.text_edit)

    def new_file(self):
        self.text_edit.clear()
        self.status_bar.showMessage("New file created", 2000) # 2000ms timeout)

if __name__ == "__main__":
    app = Widgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())