from pathlib import Path
import winreg, os, sys, shutil


class RegistryManager:
    @staticmethod
    def get_icon_path() -> Path:
        if getattr(sys, "frozen", False):
            persistent_icon_dir = Path(os.getenv("APPDATA")) / "AURA" / "icons"
            os.makedirs(persistent_icon_dir, exist_ok=True)
            persistent_icon_path = persistent_icon_dir / "icon_32.ico"
            tmp_icon_path = Path(sys._MEIPASS) / "assets" / "icon_32.ico"

            if not persistent_icon_path.exists():
                shutil.copyfile(tmp_icon_path, persistent_icon_path)

            return persistent_icon_path

        else:
            return Path(__file__).parent.parent / "assets" / "icon_32.ico"

    @staticmethod
    def associate_extension(appPath: str) -> bool:
        iconPath = RegistryManager.get_icon_path()
        try:
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, '.rskm') as key:
                winreg.SetValue(key, '', winreg.REG_SZ, 'AURA.RiskMap')

            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, 'AURA.RiskMap') as key:
                winreg.SetValue(key, '', winreg.REG_SZ, 'AURA Risk Map File')

                with winreg.CreateKey(key, 'DefaultIcon') as iconKey:
                    winreg.SetValue(iconKey, '', winreg.REG_SZ, iconPath)

                with winreg.CreateKey(key, 'shell\\open\\command') as cmdKey:
                    winreg.SetValue(cmdKey, '', winreg.REG_SZ, f'"{appPath}" "%1"')

            return True

        except PermissionError:
            return False

    @staticmethod
    def is_associated(app_path: str) -> bool:
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, '.rsk') as key:
                fileType = winreg.QueryValue(key, '')
                if fileType != 'AURA.RiskMap':
                    return False

            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f'AURA.RiskMap\\shell\\open\\command') as key:
                currentCmd = winreg.QueryValue(key, '')
                return app_path in currentCmd

        except PermissionError:
            return False