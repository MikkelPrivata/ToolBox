import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)
from PySide6.QtCore import Qt, QRect, QPoint


class FramelessWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Remove the window title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set window geometry
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Resizable Frameless Window with Custom Controls")

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Add custom title bar with buttons
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)

        # Add content area
        content = QLabel("This is a resizable frameless window. Add your content here.")
        content.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(content)

        self.setCentralWidget(central_widget)

        # Variables for resizing
        self._resizing = False
        self._dragging = False
        self._start_pos = None
        self._start_geom = None
        self._resize_margin = 5

    def create_title_bar(self):
        """Create a custom title bar with close, minimize, and maximize buttons."""
        title_bar = QWidget()
        title_layout = QHBoxLayout()
        title_bar.setLayout(title_layout)

        # Add title label
        title_label = QLabel("Custom Window")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)

        # Add spacer to push buttons to the right
        title_layout.addStretch()

        # Close button
        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("background: red; color: white; border: none;")
        title_layout.addWidget(close_button)

        # Minimize button
        minimize_button = QPushButton("_")
        minimize_button.setFixedSize(30, 30)
        minimize_button.clicked.connect(self.showMinimized)
        minimize_button.setStyleSheet("background: gray; color: white; border: none;")
        title_layout.addWidget(minimize_button)

        # Maximize/Restore button
        self.maximize_button = QPushButton("⬜")
        self.maximize_button.setFixedSize(30, 30)
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.maximize_button.setStyleSheet("background: gray; color: white; border: none;")
        title_layout.addWidget(self.maximize_button)

        return title_bar

    def toggle_maximize_restore(self):
        """Toggle between maximized and normal state."""
        if self.isMaximized():
            self.showNormal()
            self.maximize_button.setText("⬜")  # Restore icon
        else:
            self.showMaximized()
            self.maximize_button.setText("❐")  # Maximize icon

    def mousePressEvent(self, event):
        """Handle mouse press for resizing and dragging."""
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            if self.is_on_edge(pos):
                self._resizing = True
                self._start_geom = self.geometry()
                self._start_pos = event.globalPos()
            else:
                self._dragging = True
                self._start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle window dragging and resizing."""
        if self._resizing:
            self.resize_window(event.globalPos())
        elif self._dragging:
            self.move(event.globalPos() - self._start_pos)
            event.accept()
        else:
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event):
        """Reset dragging and resizing flags."""
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self._resizing = False
            event.accept()

    def update_cursor(self, pos):
        """Update the cursor based on the position near edges."""
        if self.is_on_edge(pos):
            self.setCursor(Qt.SizeAllCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def is_on_edge(self, pos):
        """Check if the cursor is near the edges of the window."""
        geom = self.rect()
        x, y = pos.x(), pos.y()
        margin = self._resize_margin
        return (
            x < margin or x > geom.width() - margin or
            y < margin or y > geom.height() - margin
        )

    def resize_window(self, global_pos):
        """Resize the window by dragging its edges."""
        if self._start_geom and self._start_pos:
            dx = global_pos.x() - self._start_pos.x()
            dy = global_pos.y() - self._start_pos.y()
            new_geom = QRect(self._start_geom)
            new_geom.setWidth(max(100, new_geom.width() + dx))
            new_geom.setHeight(max(100, new_geom.height() + dy))
            self.setGeometry(new_geom)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FramelessWindow()
    window.show()
    sys.exit(app.exec_())
