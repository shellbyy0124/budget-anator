from qfluentwidgets import (
    FluentWindow,
    FluentIcon as fi,
    Theme,
    setTheme,
    setThemeColor
)

from PySide6.QtCore import Signal

from .pages.dashboard import Dashboard


class NewUser(FluentWindow):
    agreement_accepted = Signal()

    def __init__(self, logic, async_helper, color_theme):
        super().__init__()

        self.logic = logic
        self.async_helper = async_helper
        self.color_theme = color_theme

        self.dashboard = Dashboard(self)

        self.dashboard.agreement_accepted.connect(self.agreement_accepted.emit)

        self.init_navigation()
        self.apply_theme()
        self.apply_style()

    def init_navigation(self):
        self.addSubInterface(
            self.dashboard,
            fi.HOME.icon(
                color=self.color_theme['accent']
            ),
            "Dashboard"
        )

    def apply_theme(self):
        setTheme(Theme.AUTO)
        setThemeColor(
            self.color_theme['primary']
        )

    def apply_style(self):
        self.setStyleSheet(
            f"""
                QWidget {{
                    background-color: {self.color_theme['background']};
                }}

                QLabel#page-title {{
                    font-size: 20px;
                    font-style: italic;
                    font-weight: bold;
                    color: {self.color_theme['primary']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                }}
            """
        )

    def closeEvent(self, event):
        self.logic.close_db_connection()
        event.accept()