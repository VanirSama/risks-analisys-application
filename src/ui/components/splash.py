from src.utils.resources import RESOURCE_LOADER

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSplashScreen


class SplashScreen(QSplashScreen):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(320, 180)
        self.pixmap = QPixmap(RESOURCE_LOADER.get("LOGO_WHITE", ""))
        self.pixmap = self.pixmap.scaled(320, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(self.pixmap)