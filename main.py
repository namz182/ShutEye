"""
ShutEye - System Timer Application
A modern desktop timer application for scheduling system actions
"""
import customtkinter as ctk
from pathlib import Path
import threading
import time
from typing import Optional

# Import configuration and utilities
from src.config import ConfigManager
from src.constants import CONFIG_FILE, APP_LOGO
from src.ui.screens import SetupScreen, ActiveScreen, SettingsScreen
from src.utils import SystemActionExecutor, format_time_simple, seconds_to_hms_strings
from src.utils.system_actions import ScreenInhibitor
from src.utils.time_utils import get_end_time

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TimerApp(ctk.CTk):
    """Main application window"""

    def __init__(self):
        super().__init__()

        # Load configuration
        self.config = ConfigManager(CONFIG_FILE)

        # Window configuration
        window_config = self.config.get_window_config()
        self.title("ShutEye")
        self.geometry(f"{window_config['width']}x{window_config['height']}")
        self.resizable(window_config.get("resizable", False), True)

        # Set icon if available
        try:
            self.iconbitmap(APP_LOGO)
        except Exception:
            pass  # Icon setting failed, continue

        # Timer state variables
        timer_config = self.config.get_timer_config()
        self.total_seconds = timer_config.get("default_duration", 900)
        self.remaining_seconds = self.total_seconds
        self.is_running = False
        self.timer_thread: Optional[threading.Thread] = None
        self.selected_action = "Shutdown"
        self.keep_screen_on = False

        # Theme configuration
        theme = self.config.get_theme()
        self.primary_color = theme["primary_color"]
        self.bg_dark = theme["bg_dark"]
        self.card_bg = theme["card_bg"]

        # Configure window background
        self.configure(fg_color=self.bg_dark)

        # Screen inhibitor for keep screen on feature
        self.screen_inhibitor = ScreenInhibitor()

        # Initialize screens
        self.setup_screen = SetupScreen(self)
        self.active_screen = ActiveScreen(self)
        self.settings_screen = SettingsScreen(self)

        # Show setup screen first
        self.show_setup_screen()

        # System tray setup
        self.tray_manager = None
        self.tray_running = False
        try:
            from src.tray import TrayManager, PYSTRAY_AVAILABLE
            if PYSTRAY_AVAILABLE:
                self.tray_manager = TrayManager(self, APP_LOGO)
                self.tray_manager.setup_tray()
        except Exception as e:
            print(f"Could not setup system tray: {e}")
            import traceback
            traceback.print_exc()

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)
    
    def show_setup_screen(self) -> None:
        """Display the timer setup screen"""
        self.setup_screen.show()

    def show_active_screen(self) -> None:
        """Display the active timer screen"""
        self.active_screen.show()

    def show_settings_screen(self) -> None:
        """Display the settings screen"""
        self.settings_screen.show()

    def select_action(self, action: str) -> None:
        """Handle action selection"""
        self.selected_action = action
        # Update action cards without reloading the screen
        if hasattr(self.setup_screen, 'update_action_selection'):
            self.setup_screen.update_action_selection(action)

    def add_time(self, seconds: int) -> None:
        """Add time to the timer during setup"""
        self.total_seconds += seconds
        # Ensure time doesn't go below minimum (60 seconds)
        timer_config = self.config.get_timer_config()
        min_duration = timer_config.get("min_duration", 60)
        self.total_seconds = max(min_duration, self.total_seconds)
        self.remaining_seconds = self.total_seconds
        self.setup_screen.update_display()

    def start_timer_from_setup(self) -> None:
        """Start timer and switch to active screen"""
        self.remaining_seconds = self.total_seconds
        self.show_active_screen()
        self.start_timer()

    def change_action(self, action: str) -> None:
        """Change the selected action during countdown"""
        self.selected_action = action
        self.active_screen.status_label.configure(
            text=f"System will {self.selected_action} at {get_end_time(self.remaining_seconds)}"
        )

    def slider_changed(self, value: float) -> None:
        """Handle slider value change"""
        if not self.is_running:
            self.total_seconds = int(value)
            self.remaining_seconds = self.total_seconds
            self.active_screen.update_display()

    def add_time_active(self, seconds: int) -> None:
        """Add or subtract time during active countdown"""
        self.remaining_seconds += seconds
        # Ensure remaining time doesn't go below minimum (60 seconds)
        timer_config = self.config.get_timer_config()
        min_duration = timer_config.get("min_duration", 60)
        self.remaining_seconds = max(min_duration, self.remaining_seconds)
        self.total_seconds = max(self.total_seconds, self.remaining_seconds)
        self.active_screen.update_display()

    def start_timer(self) -> None:
        """Start the countdown timer"""
        if not self.is_running:
            self.is_running = True
            self.active_screen.update_play_pause_btn(True)
            
            # Enable screen inhibitor if keep_screen_on is enabled
            if self.keep_screen_on:
                success = self.screen_inhibitor.inhibit()
                if success:
                    print("Screen will stay on during timer")
                else:
                    print("Warning: Could not enable keep screen on")
            
            self.timer_thread = threading.Thread(target=self._countdown, daemon=True)
            self.timer_thread.start()

    def toggle_timer(self) -> None:
        """Toggle between play and pause"""
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()

    def pause_timer(self) -> None:
        """Pause the timer"""
        self.is_running = False
        self.active_screen.update_play_pause_btn(False)
        
        # Disable screen inhibitor when paused
        self.screen_inhibitor.uninhibit()

    def reset_timer(self) -> None:
        """Reset timer to initial value"""
        self.is_running = False
        self.remaining_seconds = self.total_seconds
        self.active_screen.update_play_pause_btn(False)
        self.active_screen.update_display()
        
        # Disable screen inhibitor when reset
        self.screen_inhibitor.uninhibit()

    def stop_timer(self) -> None:
        """Stop timer and return to setup"""
        self.is_running = False
        self.remaining_seconds = self.total_seconds
        
        # Disable screen inhibitor when stopped
        self.screen_inhibitor.uninhibit()
        
        self.show_setup_screen()

    def _countdown(self) -> None:
        """Countdown loop running in separate thread"""
        while self.is_running and self.remaining_seconds > 0:
            time.sleep(1)
            if self.is_running:
                self.remaining_seconds -= 1
                self.after(0, self.active_screen.update_display)

        if self.is_running and self.remaining_seconds == 0:
            self.after(0, self.execute_action)

    def execute_action(self) -> None:
        """Execute the selected system action"""
        self.is_running = False
        
        # Disable screen inhibitor before executing action
        self.screen_inhibitor.uninhibit()
        
        try:
            SystemActionExecutor.execute(self.selected_action)
        except Exception as e:
            print(f"Error executing action: {e}")

    def on_window_close(self) -> None:
        """Handle window close event - minimize to tray if available"""
        if self.tray_manager and self.tray_manager.icon:
            # Hide window and start tray icon if not already running
            self.withdraw()
            if not self.tray_running:
                import threading
                self.tray_running = True
                # Start tray in non-daemon thread to keep app alive
                tray_thread = threading.Thread(target=self._run_tray_loop, daemon=False)
                tray_thread.start()
        else:
            # No tray available, ask to quit
            if self.is_running:
                from tkinter import messagebox
                if messagebox.askyesno("Confirm", "Timer is running. Stop and exit?"):
                    self.is_running = False
                    self.quit()
            else:
                self.quit()
    
    def _run_tray_loop(self) -> None:
        """Run tray icon in a way that keeps app alive"""
        try:
            if self.tray_manager and self.tray_manager.icon:
                self.tray_manager.run_tray()
        except Exception as e:
            print(f"Tray error: {e}")


def main():
    """Main entry point"""
    app = TimerApp()
    app.mainloop()


if __name__ == "__main__":
    main()