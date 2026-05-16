__all__ = ["__title__", "__major__", "__minor__", "__micro__", "__release_level__",
           "__author__", "__organization__", "__version_info__", "__copyright__", "get_version_info"]

__title__ = "АУРА-ОПР"
__major__ = 1
__minor__ = 0
__micro__ = 3
__release_level__ = "alpha"
__author__ = "Бакулин А. М."
__organization__ = 'ФГБОУ ВО "Тольяттинский Государственный Унисверситет" (ТГУ)'
__version_info__ = (__major__, __minor__, __micro__)
__copyright__ = ""


def get_version_info() -> str:
    return  f"{__title__} {'.'.join(str(x) for x in __version_info__)}-{__release_level__}"
