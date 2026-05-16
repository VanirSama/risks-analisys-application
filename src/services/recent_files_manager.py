from src.utils.resources import RESOURCE_LOADER
from src.utils.utils import clamp, normalize_path

from pathlib import Path
from typing import Optional
import gzip, json


class RecentFilesManager:
    def __init__(self, file_path: Path | str = RESOURCE_LOADER.get("RECENT_FILES", ""), max_files: int = 40):
        self._FILE_PATH = normalize_path(file_path)
        self._MAX_FILES = clamp(max_files, min_x=1, max_x=None)
        self._recent_files: list[str] = self.load_history()

    def load_history(self)  -> Optional[list]:
        if Path(self._FILE_PATH).exists():
            with gzip.open(self._FILE_PATH, "rt", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self) -> None:
        with gzip.open(self._FILE_PATH, "wt",  encoding="utf-8") as f:
            dump = json.dumps([path for path in self._recent_files], ensure_ascii=False, indent=0)
            f.write(dump)

    def add_file(self, file_path: str | Path) -> None:
        file_path = normalize_path(file_path)

        if file_path in self._recent_files:
            self._recent_files.remove(file_path)

        self._push_item(file_path)
        self.save_history()

    def _push_item(self, item: str) -> None:
        self._recent_files.insert(0, item)
        self._recent_files = self._recent_files[:self._MAX_FILES]

    def remove_file(self, file_path: Path | str) -> None:
        file_path = normalize_path(file_path)

        if file_path in self._recent_files:
            self._recent_files.remove(file_path)
            self.save_history()

    @property
    def recent_files(self) -> list:
        return self._recent_files.copy()
