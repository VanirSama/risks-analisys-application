from pathlib import Path
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QGridLayout, QSizePolicy, QFrame, QLabel, QVBoxLayout
from typing import Callable



class RecentFilesGrid(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._grid_layout = QGridLayout(self)
        self._grid_layout.setSpacing(32)
        self._grid_layout.setContentsMargins(20, 20, 20, 20)
        self._grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.current_row = 0
        self.current_col = -1
        self._max_columns = 11
        self._parent = parent

        self._click_callback = None

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_click_callback(self, callback: Callable) -> None:
        self._click_callback = callback

    def clear(self) -> None:
        for i in reversed(range(self._grid_layout.count())):
            item = self._grid_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    self._grid_layout.removeWidget(widget)
                    widget.deleteLater()

        self.current_row = 0
        self.current_col = -1

    def add_item(self, file_path: str | Path, icon) -> None:
        self.current_col += 1
        if self.current_col >= self._max_columns:
            self.current_row += 1
            self.current_col = 0

        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background: #DCD6F7;
                border-radius: 10px; }
            QFrame:hover {
                background: #E9E4FF; }
        """)
        item.setFixedSize(140, 175)
        item.setAttribute(Qt.WA_Hover, True)

        item_layout = QVBoxLayout(item)
        item_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel()
        pixmap = icon.pixmap(QSize(128, 128))
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent;")

        file_name = QLabel(Path(file_path).name)
        file_name.setStyleSheet("""
            QLabel {
                background: transparent;
                color: #4a4a7d;
                font-size: 14px;
                font-weight: bold; }
        """)

        file_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_name.setWordWrap(True)
        file_name.setMaximumWidth(100)
        file_name.setStyleSheet("""
            QLabel {
                background: transparent;
                color: #4a4a7d;
                font-size: 12px;
                font-weight: bold; }
        """)

        item_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        item_layout.addWidget(file_name, alignment=Qt.AlignmentFlag.AlignCenter)

        item.mousePressEvent = lambda event, path=file_path: self._on_item_clicked(path)

        self._grid_layout.addWidget(item, self.current_row, self.current_col, alignment=Qt.AlignmentFlag.AlignLeft)

    def _on_item_clicked(self, file_path: Path | str) -> None:
        if self._click_callback: self._click_callback(file_path)