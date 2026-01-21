"""
System action execution module for cross-platform support
"""
import os
import platform
from typing import Callable, Optional


class SystemActionExecutor:
    """Execute system actions (shutdown, restart, sleep, etc.)"""

    @staticmethod
    def shutdown() -> None:
        """Shutdown the system"""
        system = platform.system()
        try:
            if system == "Windows":
                os.system("shutdown /s /t 0")
            elif system == "Darwin":  # macOS
                os.system("osascript -e 'tell app \"System Events\" to shut down'")
            else:  # Linux
                os.system("systemctl poweroff")
        except Exception as e:
            print(f"Error executing shutdown: {e}")

    @staticmethod
    def restart() -> None:
        """Restart the system"""
        system = platform.system()
        try:
            if system == "Windows":
                os.system("shutdown /r /t 0")
            elif system == "Darwin":
                os.system("osascript -e 'tell app \"System Events\" to restart'")
            else:
                os.system("systemctl reboot")
        except Exception as e:
            print(f"Error executing restart: {e}")

    @staticmethod
    def sleep() -> None:
        """Put system to sleep"""
        system = platform.system()
        try:
            if system == "Windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif system == "Darwin":
                os.system("pmset sleepnow")
            else:
                os.system("systemctl suspend")
        except Exception as e:
            print(f"Error executing sleep: {e}")

    @staticmethod
    def lock() -> None:
        """Lock the screen"""
        system = platform.system()
        try:
            if system == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
            elif system == "Darwin":
                os.system("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend")
            else:
                os.system("loginctl lock-session")
        except Exception as e:
            print(f"Error executing lock: {e}")

    @staticmethod
    def logout() -> None:
        """Log out current user"""
        system = platform.system()
        try:
            if system == "Windows":
                os.system("shutdown /l")
            elif system == "Darwin":
                os.system("osascript -e 'tell app \"System Events\" to log out'")
            else:
                os.system("loginctl terminate-user $USER")
        except Exception as e:
            print(f"Error executing logout: {e}")

    @staticmethod
    def execute(action: str) -> None:
        """Execute action by name"""
        actions = {
            "Shutdown": SystemActionExecutor.shutdown,
            "Restart": SystemActionExecutor.restart,
            "Sleep": SystemActionExecutor.sleep,
            "Lock": SystemActionExecutor.lock,
            "Log Out": SystemActionExecutor.logout,
        }
        
        if action in actions:
            actions[action]()
        else:
            raise ValueError(f"Unknown action: {action}")
