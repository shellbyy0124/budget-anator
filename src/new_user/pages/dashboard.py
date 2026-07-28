from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
    QSlider
)
from PySide6.QtCore import Qt, QTimer, Signal


class Dashboard(QWidget):
    agreement_accepted = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Dashboard')

        self.logic = parent.logic
        self.color_theme = parent.color_theme
        self.async_helper = parent.async_helper

        self.status_bar = QStatusBar()

        self.agreements = {
            "read_write": 0,
            "browser_use": 0
        }

        self.setup_ui()
        self.apply_style()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        title = QLabel("Welcome to Budget-anator")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)

        sub_title = QLabel(
            "an application designed to assist the every day "
            "delivery driver in tracking their bills on a per/day "
            "basis"
        )
        sub_title.setObjectName("page-sub-title")
        sub_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(sub_title)

        layout.addWidget(title_container)

        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)
        body_layout.setContentsMargins(0, 10, 0, 10)
        body_layout.setSpacing(15)

        title1 = "Safety & Security"
        title2 = "How It Works"
        title3 = "User Authentication"

        text1 = (
            "This application runs entirely offline and requires no "
            "login credentials. All data you enter is stored locally "
            "on your device at \"/home/<user>/.meks-apps/budget-anator\". "
            "You can view the database file "
            "budget-anator/main.db using any SQLite database viewer."
        )

        text2 = (
            "The app calculates your daily savings target by taking "
            "your bill amount and due date, then dividing the total "
            "by the number of actual working days available before the "
            "bill is due. You can set how many days per week you "
            "work(from 1 to 7), and this number is subtracted from the "
            "total days remaining to give you a personalized \"dollars-per-"
            "working-day\" figure. Your work-week preference can be updated "
            "at any time."
        )

        text3 = (
            "Your first line of defense is you. Since this app has no "
            "internet connection, your data never leaves your device — "
            "it's not stored in the cloud or transmitted anywhere. The "
            "only ways someone could access your data are if you share "
            "your device, or if your computer is compromised (in which "
            "case you should contact your IT department immediately)."
        )

        self.create_card(body_layout, title1, text1)
        self.create_card(body_layout, title2, text2)
        self.create_card(body_layout, title3, text3)

        layout.addWidget(body_container, 2)

        promise_label = QLabel(
            "Budget-anator will NEVER operate on your system "
            "without your expressed permission!"
        )
        promise_label.setObjectName("page-sub-title")
        promise_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(promise_label)

        agreement_container = QWidget()
        agreement_layout = QVBoxLayout(agreement_container)
        agreement_layout.setContentsMargins(0, 10, 0, 10)
        agreement_layout.setSpacing(10)

        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        row1_layout.setContentsMargins(10, 0, 10, 0)
        row1_layout.setSpacing(30)

        rw_label = QLabel(
            "This application will not run without your consent "
            "to read/write to its own database, and update its "
            "files and contents therein if/when an update comes "
            "available"
        )
        rw_label.setObjectName("form-label")
        rw_label.setAlignment(Qt.AlignmentFlag.AlignVCenter |
                              Qt.AlignmentFlag.AlignLeft)
        rw_label.setWordWrap(True)
        row1_layout.addWidget(rw_label, 3)

        self.rw_slider = QSlider(Qt.Horizontal)
        self.rw_slider.setRange(0, 1)
        self.rw_slider.setValue(self.agreements.get("read_write"))
        self.rw_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.rw_slider.setTickInterval(1)
        self.rw_slider.setFixedWidth(80)
        self.rw_slider.setFixedHeight(30)
        self.rw_slider.valueChanged.connect(self.update_rw_perms)
        self.rw_slider.valueChanged.connect(self.update_slider_style)
        row1_layout.addWidget(self.rw_slider)

        agreement_layout.addWidget(row1)

        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setContentsMargins(10, 0, 10, 0)
        row2_layout.setSpacing(30)

        browser_label = QLabel(
            "This application requests permission to use your "
            "browser in the event you request support or would "
            "like to view more information about the application "
            "and its developers. This is solely to assist you in "
            "navigating to these pages versus manually searching "
            "for them"
        )
        browser_label.setObjectName("form-label")
        browser_label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        browser_label.setWordWrap(True)
        row2_layout.addWidget(browser_label, 3)

        self.browser_slider = QSlider(Qt.Horizontal)
        self.browser_slider.setRange(0, 1)
        self.browser_slider.setValue(self.agreements.get("browser_use"))
        self.browser_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.browser_slider.setTickInterval(1)
        self.browser_slider.setFixedWidth(80)
        self.browser_slider.setFixedHeight(30)
        self.browser_slider.valueChanged.connect(self.update_browser_perms)
        self.browser_slider.valueChanged.connect(self.update_slider_style)
        row2_layout.addWidget(self.browser_slider)

        agreement_layout.addWidget(row2)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFixedWidth(150)
        self.submit_btn.setEnabled(False)
        self.submit_btn.clicked.connect(self.submit_agreements)

        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 10, 0, 0)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(self.submit_btn)

        layout.addWidget(agreement_container)
        layout.addWidget(btn_container)
        layout.addWidget(self.status_bar)

    def create_card(self, layout, title: str, text: str):
        card = QWidget()
        card.setObjectName("card")
        card.setFixedSize(250, 280)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("card-title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)

        card_body = QWidget()
        card_body_layout = QVBoxLayout(card_body)
        card_body_layout.setContentsMargins(5, 5, 5, 5)
        card_body_layout.setSpacing(0)

        card_text = QLabel(text)
        card_text.setObjectName("card-text")
        card_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_text.setWordWrap(True)
        card_body_layout.addWidget(card_text)

        card_layout.addWidget(card_body, 1)
        layout.addWidget(card) 

    def apply_style(self):
        self.setStyleSheet(
            f"""
                QWidget {{
                    background-color: transparent;
                    border: none;
                }}

                QLabel#page-sub-title {{
                    font-size: 14px;
                    font-style: italic;
                    color: {self.color_theme['text_secondary']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                }}

                QWidget#card {{
                    border: 2px solid {self.color_theme['accent']};
                    border-radius: 8px;
                    background-color: {self.color_theme['surface']};
                }}

                QLabel#card-title {{
                    font-weight: bold;
                    font-style: italic;
                    font-size: 16px;
                    color: {self.color_theme['primary']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    text-decoration: underline;
                }}

                QLabel#card-text {{
                    font-style: italic;
                    font-size: 12px;
                    color: {self.color_theme['text_muted']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                }}

                QPushButton {{
                    background-color: #808080;
                    color: #404040;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 14px;
                }}

                QPushButton:enabled {{
                    background-color: #4CAF50;
                    color: white;
                }}

                QPushButton:hover:enabled {{
                    background-color: #45a049;
                }}

                QSlider::groove:horizontal {{
                    height: 20px;
                    border-radius: 10px;
                }}

                QSlider::handle:horizontal {{
                    background: {self.color_theme['text_primary']};
                    width: 20px;
                    height: 20px;
                    margin: -2px 0;
                    border-radius: 10px;
                }}

                QSlider::sub-page:horizontal {{
                    background: {self.color_theme['accent']};
                    border-radius: 10px;
                }}
            """
        )
        self.update_slider_style()

    def update_slider_style(self):
        rw_color = "#4CAF50" if self.rw_slider.value() == 1 else "#808080"
        browser_color = "#4CAF50" if self.browser_slider.value() == 1 else "#808080"

        self.rw_slider.setStyleSheet(
            f"""
                QSlider::groove:horizontal {{
                    height: 20px;
                    border-radius: 10px;
                    background: {rw_color};
                }}
                QSlider::handle:horizontal {{
                    background: {self.color_theme['text_primary']};
                    width: 20px;
                    height: 20px;
                    margin: -2px 0;
                    border-radius: 10px;
                }}
                QSlider::sub-page:horizontal {{
                    background: {rw_color};
                    border-radius: 10px;
                }}
            """
        )

        self.browser_slider.setStyleSheet(
            f"""
                QSlider::groove:horizontal {{
                    height: 20px;
                    border-radius: 10px;
                    background: {browser_color};
                }}
                QSlider::handle:horizontal {{
                    background: {self.color_theme['text_primary']};
                    width: 20px;
                    height: 20px;
                    margin: -2px 0;
                    border-radius: 10px;
                }}
                QSlider::sub-page:horizontal {{
                    background: {browser_color};
                    border-radius: 10px;
                }}
            """
        )

    def update_rw_perms(self, value):
        self.agreements["read_write"] = value
        self.submit_btn.setEnabled(value == 1)

    def update_browser_perms(self, value):
        self.agreements["browser_use"] = value

    def handle_error_success(self, msg: str, is_error: bool = None):
        if is_error is None:
            background = self.color_theme["warning"]
            border = "orange"
            delay = 3000

        elif is_error:
            background = self.color_theme['error']
            border = "red"
            delay = 4000

        else:
            background = self.color_theme['success']
            border = "green"
            delay = 5000

        self.status_bar.setStyleSheet(
            f"""
                QStatusBar {{
                    background-color: {background}
                    border: 2px solid {border}
                    color: black;
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                }}
            """
        )
        self.status_bar.showMessage(msg)

        QTimer.singleShot(delay, self.reset_status_bar)

    def reset_status_bar(self):
        self.status_bar.clearMessage()
        self.status_bar.setStyleSheet("")

    def submit_agreements(self):
        prepared_agreements = {
            "read_write": 1 if self.agreements["read_write"] == 1 else 0,
            "browser_use": 1 if self.agreements["browser_use"] == 1 else 0
        }

        worker = self.async_helper.run_async(
            self.logic.update_user_agreement,
            prepared_agreements
        )

        worker.signals.started.connect(
            lambda: self.handle_error_success("updating agreement", None)
        )
        worker.signals.finished.connect(self.update_response)
        worker.signals.error.connect(self.update_error)

    def update_response(self, did_update):
        if not did_update:
            return self.handle_error_success("failed to update agreement", True)

        self.handle_error_success("agreement updated", False)
        self.agreement_accepted.emit()

    def update_error(self, error):
        return self.handle_error_success("failed to update agreement", True)