from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap

import sys

from .config import Config
from .core.logic import Logic
from .core.utils.async_helper import AsyncHelper
from .core.utils.color_theme import COLOR_THEME
from .new_user.app import NewUser
from .app.app import Budgetanator


def run_new_user(logic, async_helper, color_theme, icon_path):
    window = NewUser(logic, async_helper, color_theme)
    window.setWindowIcon(QPixmap(icon_path))
    window.setMinimumWidth(1000)
    window.setMinimumHeight(750)
    return window


def run_main_app(logic, async_helper, color_theme, icon_path):
    window = Budgetanator(logic, async_helper, color_theme)
    window.setWindowIcon(QPixmap(icon_path))
    window.setMinimumWidth(1000)
    window.setMinimumHeight(750)
    return window


def main():
    app = QApplication(sys.argv)

    app_dir = Config.APP_DIR
    icon_path = Config.ICON_PATH
    logic = Logic(app_dir)
    async_helper = AsyncHelper()
    color_theme = COLOR_THEME

    user_agree = logic.check_user_agreement()

    if not user_agree:
        window = run_new_user(logic, async_helper, color_theme, icon_path)

        def on_agreement():
            window.close()
            main_win = run_main_app(
                logic, async_helper, color_theme, icon_path)
            main_win.show()

        window.agreement_accepted.connect(on_agreement)
    else:
        window = run_main_app(logic, async_helper, color_theme, icon_path)

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
