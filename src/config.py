"""
Configuration management module
"""
import json
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """Manages application configuration from JSON file"""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file: {self.config_path}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_app_info(self) -> Dict[str, str]:
        """Get app information (name, version, description)"""
        return self.config.get("app", {})

    def get_developer_info(self) -> Dict[str, str]:
        """Get developer information"""
        return self.config.get("developer", {})

    def get_theme(self) -> Dict[str, str]:
        """Get theme configuration"""
        return self.config.get("theme", {})

    def get_actions(self) -> list:
        """Get available system actions"""
        return self.config.get("actions", [])

    def get_quick_times(self) -> list:
        """Get quick time presets"""
        return self.config.get("quick_times", [])

    def get_window_config(self) -> Dict[str, Any]:
        """Get window configuration"""
        return self.config.get("window", {})

    def get_timer_config(self) -> Dict[str, Any]:
        """Get timer configuration"""
        return self.config.get("timer", {})
