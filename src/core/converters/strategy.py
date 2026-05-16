from src.core.converters.base import Converter
from src.core.converters.docx import RiskMapToDocxConverter
from src.core.converters.pdf import RiskMapToPdfConverter
from typing import Type


class ConverterStrategy:
    _registry = {}

    @classmethod
    def get_converter_by_filter(cls, filter_string: str) -> Type[Converter] | None:
        return cls._registry.get(filter_string, None)

    @classmethod
    def get_all_filters(cls) -> str:
        return ";;".join(cls._registry.keys())

    @classmethod
    def create_converter(cls, filter_string: str, item):
        converter_class = cls.get_converter_by_filter(filter_string)
        if converter_class:
            return converter_class(item)
        return None


class RiskMapConverterStrategy(ConverterStrategy):
    _registry: dict[str, tuple[Type[Converter], str]] = {
        # filter_string: ConverterClass
        "Документы MS Word (*.docx)":   RiskMapToDocxConverter,
        "Документы PDF (*.pdf)":        RiskMapToPdfConverter,
    }