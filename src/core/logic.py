from pathlib import Path

import json
import os

# from .database.db import get_engine, get_base, get_db


class Logic:
    def __init__(self, app_dir):
        self.app_dir = Path(app_dir)
        self.config_file = self.app_dir / "config.json"
        self.db = None

    def check_user_agreement(self) -> bool:
        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

        except FileNotFoundError:
            return False

        except (KeyError, json.JSONDecodeError):
            return False

        except Exception as e:
            print(f"Unknown Exception Reading Config:\n{e}")
            return False

        else:
            return data["read_write"] == 1

    def update_user_agreement(self, agreement_dict: dict[str, int]) -> bool:
        if not agreement_dict:
            return False

        self.app_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        except (KeyError, json.JSONDecodeError):
            if self.config_file.exists():
                os.remove(self.config_file)
            data = {}
        except Exception as e:
            print(f"Unknown Exception Reading Config:\n{e}")
            return False

        data.update(agreement_dict)  # Update instead of overwrite

        try:
            with open(self.config_file, 'w', encoding="utf-8-sig") as u:
                json.dump(data, u, indent=2)
            return True
        except Exception as e:
            print(f"Unknown Exception Writing Config:\n{e}")
            return False

    def init_db(self):
        # get_base().metadata.create_all(bind=get_engine())
        pass

    def get_db_connection(self):
        # if self.db is None:
        #     self.db = next(get_db())

        # return self.db
        pass

    def close_db_connection(self):
        # if self.db:
        #     self.db.close()
        #     self.db = None
        pass