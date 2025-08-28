from .ui import CameraUI
_ui = None
def launch():
    global _ui
    if _ui and _ui.is_alive():
        _ui.raise_window(); return _ui
    _ui = CameraUI()
    return _ui.create_ui()