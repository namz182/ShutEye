"""
System action execution module for cross-platform support
"""
import os
import platform
import subprocess
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


class ScreenInhibitor:
    """Prevent screen from turning off or locking"""
    
    def __init__(self):
        self.system = platform.system()
        self.process = None
        self.is_inhibited = False
    
    def inhibit(self) -> bool:
        """Prevent screen from turning off"""
        if self.is_inhibited:
            return True
        
        try:
            if self.system == "Linux":
                return self._inhibit_linux()
            elif self.system == "Darwin":
                return self._inhibit_macos()
            elif self.system == "Windows":
                return self._inhibit_windows()
        except Exception as e:
            print(f"Failed to inhibit screen: {e}")
            return False
        
        return False
    
    def uninhibit(self) -> None:
        """Allow screen to turn off normally"""
        if not self.is_inhibited:
            return
        
        try:
            if self.system == "Linux":
                self._uninhibit_linux()
            elif self.system == "Darwin":
                self._uninhibit_macos()
            elif self.system == "Windows":
                self._uninhibit_windows()
        except Exception as e:
            print(f"Failed to uninhibit screen: {e}")
        
        self.is_inhibited = False
    
    def _inhibit_linux(self) -> bool:
        """Linux-specific screen inhibit using systemd-inhibit or xdg-screensaver"""
        # Try systemd-inhibit first (modern approach)
        try:
            # Check if systemd-inhibit is available
            result = subprocess.run(
                ["which", "systemd-inhibit"],
                capture_output=True,
                timeout=2
            )
            
            if result.returncode == 0:
                # Use systemd-inhibit to prevent idle/sleep
                self.process = subprocess.Popen(
                    [
                        "systemd-inhibit",
                        "--what=idle:sleep",
                        "--who=ShutEye",
                        "--why=Timer is active",
                        "--mode=block",
                        "sleep", "infinity"
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.is_inhibited = True
                return True
        except Exception:
            pass
        
        # Fallback to xdg-screensaver
        try:
            subprocess.run(
                ["xdg-screensaver", "suspend", str(os.getpid())],
                check=True,
                timeout=2
            )
            self.is_inhibited = True
            return True
        except Exception:
            pass
        
        return False
    
    def _uninhibit_linux(self) -> None:
        """Linux-specific uninhibit"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
            self.process = None
        
        # Also try to resume xdg-screensaver
        try:
            subprocess.run(
                ["xdg-screensaver", "resume", str(os.getpid())],
                timeout=2
            )
        except Exception:
            pass
    
    def _inhibit_macos(self) -> bool:
        """macOS-specific screen inhibit using caffeinate"""
        try:
            self.process = subprocess.Popen(
                ["caffeinate", "-d"],  # -d prevents display from sleeping
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_inhibited = True
            return True
        except Exception as e:
            print(f"Failed to start caffeinate: {e}")
            return False
    
    def _uninhibit_macos(self) -> None:
        """macOS-specific uninhibit"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
            self.process = None
    
    def _inhibit_windows(self) -> bool:
        """Windows-specific screen inhibit using SetThreadExecutionState"""
        try:
            import ctypes
            ES_CONTINUOUS = 0x80000000
            ES_DISPLAY_REQUIRED = 0x00000002
            ES_SYSTEM_REQUIRED = 0x00000001
            
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED
            )
            self.is_inhibited = True
            return True
        except Exception as e:
            print(f"Failed to set Windows execution state: {e}")
            return False
    
    def _uninhibit_windows(self) -> None:
        """Windows-specific uninhibit"""
        try:
            import ctypes
            ES_CONTINUOUS = 0x80000000
            
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        except Exception as e:
            print(f"Failed to reset Windows execution state: {e}")
