"""
Application constants and configuration paths
"""
import os
from pathlib import Path

# Base directory paths
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
IMG_DIR = ASSETS_DIR / "img"
CONFIG_FILE = BASE_DIR / "config.json"

# Icon paths
ICON_POWER = str(ICONS_DIR / "power.png")
ICON_REDO = str(ICONS_DIR / "redo.png")
ICON_MOON = str(ICONS_DIR / "moon-sleep.png")
ICON_STOPWATCH = str(ICONS_DIR / "stopwatch.png")
ICON_STOP = str(ICONS_DIR / "stop.png")
ICON_SETTINGS = str(ICONS_DIR / "settings.png")
ICON_PLAY = str(ICONS_DIR / "play.png")
ICON_CHECK = str(ICONS_DIR / "check-fill.png")
ICON_BACK = str(ICONS_DIR / "navigate-back.png")
ICON_LOGOUT = str(ICONS_DIR / "logout.png")
ICON_LOCK = str(ICONS_DIR / "lock.png")

# App logo
APP_LOGO = str(IMG_DIR / "clock-logo.png")

# Icon mapping
ICON_MAP = {
    "power": ICON_POWER,
    "redo": ICON_REDO,
    "moon": ICON_MOON,
    "stopwatch": ICON_STOPWATCH,
    "stop": ICON_STOP,
    "settings": ICON_SETTINGS,
    "play": ICON_PLAY,
    "check": ICON_CHECK,
    "back": ICON_BACK,
    "logout": ICON_LOGOUT,
    "lock": ICON_LOCK,
}

# Action-to-icon mapping
ACTION_ICONS = {
    "Shutdown": ICON_POWER,
    "Restart": ICON_REDO,
    "Sleep": ICON_MOON,
    "Lock": ICON_LOCK,
    "Log Out": ICON_LOGOUT,
}
