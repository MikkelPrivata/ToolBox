import os
import sys
import json
from PySide6 import QtWidgets as Widgets, QtGui as GUI
from PySide6.QtWidgets import QTextEdit as TextEdit, QMenuBar as MenuBar, QStatusBar as StatusBar, QMessageBox as MessageBox
from PySide6.QtGui import QAction as Action, QFont as Font, QIcon as Icon, QTextCursor as TextCursor, QTextCharFormat as TextCharFormat, QGuiApplication as GuiApplication

short_message_duration = 2000 # milliseconds
toolbox_name = "TOOLBOX"
text_editor_name = "Texty"
toolbox_text_editor_title = toolbox_name + " | " + text_editor_name

class MainWindow(Widgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.document_modified = False
        self.file_path = None
        self.file_extension = ".txty"

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
        
        file_menu.addAction(new_action);        new_action.triggered.connect(self.new_file)
        file_menu.addAction(open_action);       open_action.triggered.connect(self.open_file)
        file_menu.addAction(save_action);       save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_as_action);    save_as_action.triggered.connect(self.save_file_as)

        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        #--------------------------------------------------------------
        #> TOOLBAR
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)
        
            #> Bold <#
        self.bold_action = Action("Bold", self)
        self.bold_action.setIcon(Icon.fromTheme("format-text-bold"))
        # custom_bold_icon = Icon("DALL-E me.png")
        # self.bold_action.setIcon(custom_bold_icon)
        self.bold_action.setShortcut(GUI.QKeySequence("Ctrl+B"))
        self.bold_action.setToolTip("Make selected text bold\nShortcut: Ctrl+B")
        self.bold_action.triggered.connect(self.make_bold)

            #> Italic <#
        self.italic_action = Action("Italic", self)
        self.italic_action.setIcon(Icon.fromTheme("format-text-italic"))
        self.italic_action.setShortcut(GUI.QKeySequence("Ctrl+I"))
        self.italic_action.setToolTip("Make selected text italic\nShortcut: Ctrl+I")
        self.italic_action.triggered.connect(self.make_italic)

            #> Underline <#
        self.underline_action = Action("Underline", self)
        self.underline_action.setIcon(Icon.fromTheme("format-text-underline"))
        self.underline_action.setShortcut(GUI.QKeySequence("Ctrl+U"))
        self.underline_action.setToolTip("Make selected text underline\nShortcut: Ctrl+U")
        self.underline_action.triggered.connect(self.make_underline)


        self.toolbar.addAction(self.bold_action)
        self.toolbar.addAction(self.italic_action)
        self.toolbar.addAction(self.underline_action)


        #--------------------------------------------------------------
        #> TEXT EDIT FIELD
        self.file_name = "Untitled"
        self.set_window_title(toolbox_text_editor_title + " - " + self.file_name)

        self.text_edit_field = TextEdit(self)
        self.text_edit_field.setGeometry(50, 50, 700, 500)
        self.cursor = TextCursor(self.text_edit_field.document())

        font = GUI.QFont("Courier New", 12)
        self.text_edit_field.setFont(font)

        self.text_edit_field.textChanged.connect(self.on_text_changed)
        self.text_edit_field.selectionChanged.connect(self.update_toolbar_actions)

        self.setCentralWidget(self.text_edit_field)


    # def clear_formatting(self):
    #     cursor = self.text_edit_field.textCursor()
    #     cursor.select(TextCursor.Document)
    #     cursor.removeSelectedText()
    #     cursor.insertText(self.text_edit_field.toPlainText())  # Re-insert as plain text
    #     cursor.setCharFormat(TextCharFormat())

    def clear_formatting(self):
        cursor = self.text_edit_field.textCursor()
        cursor.select(TextCursor.Document)
        char_format = TextCharFormat()
        cursor.setCharFormat(char_format)


    def make_bold(self):
        print("Bold action triggered")
        cursor = self.text_edit_field.textCursor()
        if not cursor.hasSelection():
            return
        char_format = TextCharFormat()
        char_format.setFontWeight(Font.Bold if not cursor.charFormat().fontWeight() == Font.Bold else Font.Normal)
        cursor.mergeCharFormat(char_format)

    def make_italic(self):
        print("Italic action triggered")
        cursor = self.text_edit_field.textCursor()
        if not cursor.hasSelection():
            return

        char_format = TextCharFormat()
        char_format.setFontItalic(not cursor.charFormat().fontItalic())
        cursor.mergeCharFormat(char_format)

    def make_underline(self):
        print("Underline action triggered")
        cursor = self.text_edit_field.textCursor()
        if not cursor.hasSelection():
            return

        char_format = TextCharFormat()
        char_format.setFontUnderline(not cursor.charFormat().fontUnderline())
        cursor.mergeCharFormat(char_format)


    def set_window_title(self, title):
        self.setWindowTitle(title)


    def on_text_changed(self):
        if not self.document_modified:
            self.document_modified = True
            self.update_window_title()

    def update_toolbar_actions(self):
        cursor = self.text_edit_field.textCursor()

        is_bold = cursor.charFormat().fontWeight() == Font.Bold

    def update_window_title(self):
        modified_indicator = "*" if self.document_modified else ""
        self.set_window_title(toolbox_text_editor_title + " - " + self.file_name + " " + modified_indicator)


    def new_file(self):
        if self.document_modified:
            reply = self.display_unsaved_changes_message(None)
            if reply == MessageBox.Cancel:
                return
        self.text_edit_field.clear()
        self.document_modified = False

        self.file_name = "Untitled"
        self.set_window_title(toolbox_text_editor_title + " - " + self.file_name)

        self.status_bar.showMessage("New file created", short_message_duration)


    def open_file(self):
        if self.document_modified:
            reply = self.display_unsaved_changes_message(None)
            if reply == MessageBox.Cancel:
                return
        file_path, _ = Widgets.QFileDialog.getOpenFileName(self, "Open File",
                                                                 "",
                                                                 "All supported files (*.txty *.txt);;" \
                                                                 "Texty Files (*.txty);;" \
                                                                 "Text Files (*.txt)" \
                                                                 "All Files (*)"
                                                                 )
        self.file_path = file_path

        if file_path: #checks whether a file was selected
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == ".txty":
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    content = data['content']
                    formatting = data.get('formatting', [])
                    self.clear_formatting()
                    self.text_edit_field.setPlainText(content)

                    cursor = self.text_edit_field.textCursor()
                    for format_data in formatting:
                        start, end = format_data["range"]
                        cursor.setPosition(start)
                        cursor.setPosition(end, TextCursor.MoveMode.KeepAnchor)
                        char_format = TextCharFormat()

                        if format_data.get("bold", False):
                            char_format.setFontWeight(Font.Bold)

                        if format_data.get("italic", False):
                            char_format.setFontItalic(True)

                        if format_data.get("underline", False):
                            char_format.setFontUnderline(True)

                        cursor.setCharFormat(char_format)

                    self.status_bar.showMessage(f"Opened file : {file_path}", short_message_duration)

            elif file_extension == ".txt":
                with open(file_path, 'r') as file:
                    content = file.read()
                self.clear_formatting()
                self.text_edit_field.setPlainText(content)
                self.status_bar.showMessage(f"Opened file : {file_path}", short_message_duration)
            else:
                self.status_bar.showMessage(f"Unsupported file type: {file_path}", short_message_duration)

            self.file_name = os.path.basename(file_path)
            self.set_window_title(toolbox_text_editor_title + " - " + self.file_name)
            self.document_modified = False
    
    def save_file(self):
        if not self.file_path:
            file_path, _ = Widgets.QFileDialog.getSaveFileName(self, f"Save File", self.file_name, "Texty Files (*.txty);;Text Files (*.txt);;All Files (*)")
            self.file_path = file_path
        self.write_file(self.file_path)

    def save_file_as(self):
        file_path, _ = Widgets.QFileDialog.getSaveFileName(self, f"Save File As", self.file_name, "Texty Files (*.txty);;Text Files (*.txt);;All Files (*)")
        self.file_path = file_path
        self.write_file(self.file_path)

    def write_file(self, file_path):
        file_extension = os.path.splitext(file_path)[1].lower()

        if not file_extension:
            file_path += ".txty"
            file_extension = ".txty"

        content = self.text_edit_field.toPlainText()

        if file_extension == ".txty":
            data = {
                "metadata": {"title": self.file_name},
                "content": content,
                "formatting": self.get_formatting()
            }
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            self.status_bar.showMessage(f"File saved as .txty: {file_path}", short_message_duration)
        elif file_extension == ".txt":
            with open(file_path, 'w') as file:
                file.write(content)
            self.status_bar.showMessage(f"File saved as .txt: {file_path}", short_message_duration)
        else:
            self.status_bar.showMessage(f"Unsupported file type: {file_path}", short_message_duration)
            return
        
        self.document_modified = False
        self.update_window_title()


    def get_formatting(self):
        formatting = []
        cursor = self.text_edit_field.textCursor()
        cursor.movePosition(TextCursor.MoveOperation.Start)

        current_format = None
        start_position = None

        while True:
            if cursor.position() >= self.text_edit_field.document().characterCount() - 1:
                break

            # Get the character's format
            char_format = cursor.charFormat()
            new_format = {
                "bold": char_format.fontWeight() == Font.Bold,
                "italic": char_format.fontItalic(),
                "underline": char_format.fontUnderline()
            }

            # Check if the format has changed
            if current_format != new_format:
                # Save the previous range if a format was being tracked
                if current_format is not None and start_position is not None:
                    formatting.append({
                        **current_format,
                        "range": [start_position, cursor.position()]
                    })
                
                # Update the current format and start position
                current_format = new_format
                start_position = cursor.position()
            
            # Move to the next character
            cursor.movePosition(TextCursor.MoveOperation.NextCharacter)

        # Handle the final range
        if current_format is not None and start_position is not None:
            formatting.append({
                **current_format,
                "range": [start_position, cursor.position()]
            })

        return formatting

    def closeEvent(self, event):
        if self.document_modified:
            self.display_unsaved_changes_message(event)
        else:
            event.accept()

    def display_unsaved_changes_message(self, event):
        reply = MessageBox.question(
            self,
            "Unsaved Changes",
            "You have unsaved changes. Do you want to save them before closing?",
            MessageBox.Yes | MessageBox.No | MessageBox.Cancel,
            MessageBox.Cancel
        )

        if reply == MessageBox.Yes:
            self.save_file()
            if event:
                event.accept()
        elif reply == MessageBox.No:
            if event:
                event.accept()
        elif event:
            event.ignore()

        return reply

if __name__ == "__main__":
    app = Widgets.QApplication(sys.argv)
    main_window = MainWindow()

    screens = GuiApplication.screens()
    if len(screens) > 2:
        secondary_screen = screens[2]
        screen_geometry = secondary_screen.geometry()

        x = screen_geometry.x() + (screen_geometry.width() - main_window.width()) // 2
        y = screen_geometry.y() + (screen_geometry.height() - main_window.height()) // 2
        main_window.move(x, y)
    elif len(screens) > 1:
        secondary_screen = screens[1]
        screen_geometry = secondary_screen.geometry()

        x = screen_geometry.x() + (screen_geometry.width() - main_window.width()) // 2
        y = screen_geometry.y() + (screen_geometry.height() - main_window.height()) // 2
        main_window.move(x, y)
    else:
        print("Only one monitor detected, opening on the primary screen.")

    main_window.show()
    sys.exit(app.exec())