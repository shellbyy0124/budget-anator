from pathlib import Path


class Config:
    APP_DIR = Path("~/.meks-apps/budget-anator").expanduser()
    ICON_PATH = Path("./src/core/assets/icon.png").expanduser()