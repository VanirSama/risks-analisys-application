from PySide6.QtCore import QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, Property
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton


class PulseAnimationMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_bg_color = QColor("#383e92")
        self._default_hover_color = QColor("#241d50")
        self._bg_color = QColor(self._default_bg_color)
        self._hover_color = QColor(self._default_hover_color)
        self._is_hovered = False
        self._animation_group: QParallelAnimationGroup | None = None
        self._update_stylesheet()

    def enterEvent(self, event):
        self._is_hovered = True
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_hovered = False
        super().leaveEvent(event)

    def _get_bg_color(self) -> QColor:
        return self._bg_color

    def _set_bg_color(self, color: QColor) -> None:
        self._bg_color = QColor(color)
        self._update_stylesheet()

    def _get_hover_color(self) -> QColor:
        return self._hover_color

    def _set_hover_color(self, hover_color: QColor) -> None:
        self._hover_color = QColor(hover_color)
        self._update_stylesheet()

    bgColor = Property(QColor, _get_bg_color, _set_bg_color)
    hoverColor = Property(QColor, _get_hover_color, _set_hover_color)

    def _update_stylesheet(self) -> None:
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._bg_color.name()};
                border-radius: 20px;
                color: #F4EEFF;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self._hover_color.name()};
                border-radius: 20px;
                color: #F4EEFF;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }}
        """)

    def _stop_current_animation(self) -> None:
        if self._animation_group and self._animation_group.state() == QParallelAnimationGroup.State.Running:
            self._animation_group.stop()
            try:
                self._animation_group.finished.disconnect()
            except RuntimeError:
                pass
            self._animation_group = None

    def pulse(self, color: QColor, fade_in: int = 300, fade_out: int = 300) -> None:
        self._stop_current_animation()

        current_bg = QColor(self._bg_color)
        current_hover = QColor(self._hover_color)

        fade_in_bg = QPropertyAnimation(self, b"bgColor")
        fade_in_bg.setDuration(fade_in)
        fade_in_bg.setStartValue(current_bg)
        fade_in_bg.setEndValue(color)
        fade_in_bg.setEasingCurve(QEasingCurve.Type.InOutQuad)

        fade_in_hover = QPropertyAnimation(self, b"hoverColor")
        fade_in_hover.setDuration(fade_in)
        fade_in_hover.setStartValue(current_hover)
        fade_in_hover.setEndValue(color)
        fade_in_hover.setEasingCurve(QEasingCurve.Type.InOutQuad)

        phase_in = QParallelAnimationGroup()
        phase_in.addAnimation(fade_in_bg)
        phase_in.addAnimation(fade_in_hover)

        fade_out_bg = QPropertyAnimation(self, b"bgColor")
        fade_out_bg.setDuration(fade_out)
        fade_out_bg.setStartValue(color)
        fade_out_bg.setEndValue(self._default_bg_color)
        fade_out_bg.setEasingCurve(QEasingCurve.Type.InOutQuad)

        fade_out_hover = QPropertyAnimation(self, b"hoverColor")
        fade_out_hover.setDuration(fade_out)
        fade_out_hover.setStartValue(color)
        fade_out_hover.setEndValue(self._default_hover_color)
        fade_out_hover.setEasingCurve(QEasingCurve.Type.InOutQuad)

        phase_out = QParallelAnimationGroup()
        phase_out.addAnimation(fade_out_bg)
        phase_out.addAnimation(fade_out_hover)

        from PySide6.QtCore import QSequentialAnimationGroup
        self._animation_group = QSequentialAnimationGroup(self)
        self._animation_group.addAnimation(phase_in)
        self._animation_group.addAnimation(phase_out)

        self._animation_group.finished.connect(self._on_animation_finished)
        self._animation_group.start()

    def _on_animation_finished(self) -> None:
        self._bg_color = QColor(self._default_bg_color)
        self._hover_color = QColor(self._default_hover_color)
        self._update_stylesheet()

    def pulse_success(self, fade_in: int = 300, fade_out: int = 300) -> None:
        self.pulse(QColor("#2ecc71"), fade_in=fade_in, fade_out=fade_out)

    def pulse_error(self, fade_in: int = 300, fade_out: int = 300) -> None:
        self.pulse(QColor("#e74c3c"), fade_in=fade_in, fade_out=fade_out)


class PulsingButton(PulseAnimationMixin, QPushButton):
    def __init__(self, text: str = "Button", parent=None) -> None:
        super().__init__(text, parent)