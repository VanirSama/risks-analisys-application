from src.utils.resources import RESOURCE_LOADER

from PySide6.QtGui import QFontDatabase


def load_fonts():
    font_id = QFontDatabase.addApplicationFont(RESOURCE_LOADER.get("STROGO_FONT", ""))
    if font_id != -1:
        Fonts.STROGO = QFontDatabase.applicationFontFamilies(font_id)[0]


class Fonts:
   STROGO = ""