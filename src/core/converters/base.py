from src.core.file_system import TFile
from src.__version__ import __title__, get_version_info

from abc import ABC, abstractmethod
from typing import Generic
from pathlib import Path


class Converter(ABC, Generic[TFile]):
    _METADATA = {
        "author": get_version_info(),
        "comments": f"Generated with {__title__}",
    }
    FILTER_STRING: str = ""
    OUTPUT_FORMAT: str = ""

    def __init__(self, file: TFile):
        self._file = file

    @abstractmethod
    def convert(self, output_path: Path | str) -> None:
        pass

    @classmethod
    def get_filter_string(cls) -> str:
        return cls.FILTER_STRING

    @classmethod
    def get_output_format(cls) -> str:
        return cls.OUTPUT_FORMAT