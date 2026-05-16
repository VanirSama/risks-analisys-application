from src.utils.utils import normalize_path

from pathlib import Path
from typing import Optional, Any
import sys, os


class ResourceLoader:
    BASE_DIR        = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(__file__).parent.parent.parent
    SRC_DIR         = BASE_DIR / "src"
    ASSETS          = SRC_DIR / "assets"
    ICONS           = ASSETS / "icons"
    FONTS           = ASSETS / "fonts"
    DATABASE        = SRC_DIR / "core" / "database"

    APPDATA         = Path(os.getenv("APPDATA")) / "AURA"
    if not APPDATA.exists(): APPDATA.mkdir(exist_ok=True)

    LOGO_WHITE      = ICONS / "logo.png"
    LOGO_COLORED    = ICONS / "logo_color.png"
    RSKM_DOC_ICON   = ICONS / "rskm_icon.png"
    RSKS_DOC_ICON   = ICONS / "rsks_icon.png"
    APP_ICON        = ICONS / "app_icon.png"

    STROGO_FONT     = FONTS / "Strogo-Regular.ttf"

    DATABASE_FILE   = DATABASE / "db.json"
    RECENT_FILES    = APPDATA / "recent_files.dat"
    CRASHLOG        = APPDATA / "crashlog.log"

    def get(self, attr: str, fallback: Optional[Any] = None) -> Any:
        if ret:=self.__getitem__(attr): return ret
        else: return fallback

    def __getitem__(self, attr: str) -> Optional[str]:
        if hasattr(self, attr): return normalize_path(getattr(self, attr))
        else: return None


RESOURCE_LOADER = ResourceLoader()
