import json
import os
from typing import Optional


class StateStore:
    def __init__(self, path: str):
            self.path = path

                def _ensure_parent_dir(self) -> None:
                        parent = os.path.dirname(self.path)
                                if parent:
                                            os.makedirs(parent, exist_ok=True)

                                                def load_last_key(self) -> Optional[str]:
                                                        if not os.path.exists(self.path):
                                                                    return None

                                                                            with open(self.path, "r", encoding="utf-8") as f:
                                                                                        data = json.load(f)

                                                                                                return data.get("last_timestamp_key")

                                                                                                    def save_last_key(self, key: str) -> None:
                                                                                                            self._ensure_parent_dir()
                                                                                                                    payload = {"last_timestamp_key": key}

                                                                                                                            with open(self.path, "w", encoding="utf-8") as f:
                                                                                                                                        json.dump(payload, f, ensure_ascii=False, indent=2)