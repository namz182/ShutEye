"""
System tray integration using pystray
"""
try:
    from pystray import Icon, Menu, MenuItem
    from PIL import Image
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False


class TrayManager:
    """Manages system tray integration"""

    def __init__(self, app, icon_path: str):
        self.app = app
        self.icon_path = icon_path
        self.icon = None

    def setup_tray(self) -> None:
        """Setup the system tray icon and menu"""
        if not PYSTRAY_AVAILABLE:
            print("pystray not available. System tray integration disabled.")
            return

        try:
            # Load icon image and convert to RGBA
            image = Image.open(self.icon_path)
            image = image.convert('RGBA')  # Ensure RGBA mode
            image = image.resize((64, 64), Image.Resampling.LANCZOS)

            # Create menu - MenuItem requires action parameter, not positional
            menu = Menu(
                MenuItem("Show Window", action=self._show_window, default=True),
                MenuItem("Hide Window", action=self._hide_window),
                Menu.SEPARATOR,
                MenuItem("Start Timer", action=self._start_timer),
                MenuItem("Pause Timer", action=self._stop_timer),
                Menu.SEPARATOR,
                MenuItem("Exit", action=self._quit_app),
            )

            # Create icon with both left-click and menu support
            self.icon = Icon(
                name="ShutEye",
                icon=image,  # Use 'icon' parameter instead of 'image'
                title="ShutEye - System Timer",
                menu=menu
            )
            
            # Set default action for left-click to show window
            self.icon._default_action = self._show_window

        except Exception as e:
            print(f"Error setting up tray: {e}")
            import traceback
            traceback.print_exc()

    def run_tray(self) -> None:
        """Run the tray icon"""
        if self.icon:
            self.icon.run()

    def stop_tray(self) -> None:
        """Stop the tray icon"""
        if self.icon and self.icon.visible:
            self.icon.stop()

    def update_tooltip(self, message: str) -> None:
        """Update the tray icon tooltip"""
        if self.icon:
            self.icon.title = message

    def _show_window(self, icon=None, item=None) -> None:
        """Show the application window"""
        def show():
            self.app.deiconify()
            self.app.lift()
            self.app.focus_force()
        # Schedule in main thread
        self.app.after(0, show)

    def _hide_window(self, icon=None, item=None) -> None:
        """Hide the application window to tray"""
        def hide():
            self.app.withdraw()
        # Schedule in main thread
        self.app.after(0, hide)

    def _start_timer(self, icon=None, item=None) -> None:
        """Start the timer from tray"""
        def start():
            if not self.app.is_running:
                self.app.show_active_screen()
                self.app.start_timer()
            self.app.deiconify()
            self.app.lift()
            self.app.focus_force()
        # Schedule in main thread
        self.app.after(0, start)

    def _stop_timer(self, icon=None, item=None) -> None:
        """Stop the timer from tray"""
        def stop():
            if self.app.is_running:
                self.app.pause_timer()
        # Schedule in main thread
        self.app.after(0, stop)

    def _quit_app(self, icon=None, item=None) -> None:
        """Quit the application"""
        def quit_app():
            self.app.is_running = False
            self.stop_tray()
            self.app.quit()
        # Schedule in main thread
        self.app.after(0, quit_app)
