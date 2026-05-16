from src.ui.styles.qss_styles import Styles

from PySide6.QtWidgets import QMessageBox


class RusMsgBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.MESSAGE_BOX)

    @staticmethod
    def critical(parent, title, message, *kwargs) -> int:
        msg = RusMsgBox(parent)

        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)

        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.button(QMessageBox.StandardButton.Ok).setText("ОК")
        return msg.exec()

    @staticmethod
    def information(parent, title, message, *kwargs) -> int:
        msg = RusMsgBox(parent)

        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)

        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.button(QMessageBox.StandardButton.Ok).setText("ОК")
        return msg.exec()

    @staticmethod
    def question(parent, title: str, message: str, *kwargs) -> int:
        msg = RusMsgBox(parent)

        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(title)
        msg.setText(message)

        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        msg.button(QMessageBox.StandardButton.Yes).setText("Да")
        msg.button(QMessageBox.StandardButton.No).setText("Нет")
        msg.button(QMessageBox.StandardButton.Cancel).setText("Отмена")
        return msg.exec()
