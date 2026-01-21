"""
Screen/Page components for the application
"""
import customtkinter as ctk
from typing import Callable, TYPE_CHECKING
from PIL import Image

from src.ui.components import (
    CTkHeader, CTkQuickButton, CTkActionCard,
    CTkTimerDisplay, CTkScrollableSection, CTkLabel
)
from src.utils.time_utils import (
    format_time_display, format_time_simple, seconds_to_hms_strings, get_end_time
)
from src.constants import ICON_SETTINGS, ICON_PLAY, ICON_CHECK, APP_LOGO
from src.config import ConfigManager

if TYPE_CHECKING:
    from main import TimerApp


class SettingsScreen:
    """Settings/About screen"""

    def __init__(self, app: "TimerApp"):
        self.app = app
        self.config = app.config

    def show(self) -> None:
        """Display the settings screen"""
        # Clear window
        for widget in self.app.winfo_children():
            widget.destroy()

        # Main container with scrollable frame
        main_container = CTkScrollableSection(
            self.app, fg_color=self.app.bg_dark
        )
        main_container.pack(fill="both", expand=True, padx=0, pady=0)

        # Header
        header = CTkHeader(
            main_container,
            title="Settings",
            left_btn_text="Back",
            left_btn_command=self.app.show_setup_screen,
            fg_color=self.app.bg_dark,
            height=60
        )
        header.pack(fill="x", padx=20, pady=20)

        # App Info Section
        app_info_label = CTkLabel(
            main_container, text="App Information",
            style="heading2", anchor="w"
        )
        app_info_label.pack(fill="x", padx=20, pady=(30, 10))

        # App Card
        app_card = ctk.CTkFrame(
            main_container, fg_color=self.app.card_bg,
            corner_radius=12
        )
        app_card.pack(fill="x", padx=20, pady=10)

        # Logo and app details
        card_inner = ctk.CTkFrame(app_card, fg_color="transparent")
        card_inner.pack(fill="x", padx=20, pady=20)

        # Logo
        try:
            logo_img = Image.open(APP_LOGO)
            logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
            logo_image = ctk.CTkImage(light_image=logo_img, size=(80, 80))
            logo_label = ctk.CTkLabel(card_inner, image=logo_image, text="")
            logo_label.image = logo_image
            logo_label.pack(pady=(0, 15))
        except Exception:
            pass

        # App name
        app_name = self.config.get("app.name", "ShutEye")
        app_name_label = CTkLabel(
            card_inner, text=app_name,
            style="heading2", anchor="center"
        )
        app_name_label.pack(fill="x", pady=5)

        # Version
        app_version = self.config.get("app.version", "1.0.0")
        version_label = CTkLabel(
            card_inner, text=f"Version {app_version}",
            style="caption", anchor="center"
        )
        version_label.pack(fill="x", pady=5)

        # Description
        app_desc = self.config.get("app.description", "")
        if app_desc:
            desc_label = CTkLabel(
                card_inner, text=app_desc,
                style="caption", anchor="center"
            )
            desc_label.pack(fill="x", pady=5)

        # Developer Section
        dev_label = CTkLabel(
            main_container, text="Developer",
            style="heading2", anchor="w"
        )
        dev_label.pack(fill="x", padx=20, pady=(30, 10))

        # Developer Card
        dev_card = ctk.CTkFrame(
            main_container, fg_color=self.app.card_bg,
            corner_radius=12
        )
        dev_card.pack(fill="x", padx=20, pady=10)

        dev_inner = ctk.CTkFrame(dev_card, fg_color="transparent")
        dev_inner.pack(fill="x", padx=20, pady=20)

        # Developer info
        dev_info = self.config.get_developer_info()

        # Name
        dev_name = dev_info.get("name", "Unknown")
        name_label = CTkLabel(
            dev_inner, text="Name",
            style="heading3", anchor="w"
        )
        name_label.pack(fill="x", pady=(0, 5))
        
        name_value = CTkLabel(
            dev_inner, text=dev_name,
            style="body", anchor="w"
        )
        name_value.pack(fill="x", padx=(20, 0), pady=(0, 10))

        # Website
        website = dev_info.get("website", "")
        if website:
            website_label = CTkLabel(
                dev_inner, text="Website",
                style="heading3", anchor="w"
            )
            website_label.pack(fill="x", pady=(0, 5))
            
            website_button = ctk.CTkButton(
                dev_inner, text=website,
                fg_color=self.app.primary_color,
                hover_color="#1557b0",
                command=lambda: self._open_website(website),
                height=40
            )
            website_button.pack(fill="x", padx=(20, 0))

        # Spacing
        ctk.CTkFrame(main_container, fg_color="transparent", height=30).pack()

    def _open_website(self, url: str) -> None:
        """Open website in browser"""
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening website: {e}")


class SetupScreen:
    """Initial timer setup screen"""

    def __init__(self, app: "TimerApp"):
        self.app = app
        self.config = app.config
        self.start_btn_setup = None

    def show(self) -> None:
        """Display the timer setup screen"""
        # Clear window
        for widget in self.app.winfo_children():
            widget.destroy()

        # Main container with scrollable frame
        main_container = CTkScrollableSection(
            self.app, fg_color=self.app.bg_dark
        )
        main_container.pack(fill="both", expand=True, padx=0, pady=0)

        # Header
        header = CTkHeader(
            main_container,
            title="New Timer Setup",
            right_btn_text="Settings",
            right_btn_command=self.app.show_settings_screen,
            fg_color=self.app.bg_dark,
            height=60
        )
        header.pack(fill="x", padx=20, pady=(20, 10))

        # Time Display
        time_frame = ctk.CTkFrame(main_container, fg_color=self.app.bg_dark)
        time_frame.pack(pady=30)

        self.setup_time_display = CTkLabel(
            time_frame, text=format_time_display(self.app.total_seconds),
            style="heading1"
        )
        self.setup_time_display.pack()

        time_label = CTkLabel(
            time_frame, text="HOURS : MINUTES : SECONDS",
            style="caption"
        )
        time_label.pack(pady=(5, 0))

        # +/- Buttons for 1 minute adjustment
        adjust_frame = ctk.CTkFrame(main_container, fg_color=self.app.bg_dark)
        adjust_frame.pack(pady=10)

        minus_btn = ctk.CTkButton(
            adjust_frame, text="-", width=60, height=40,
            fg_color=self.app.card_bg, hover_color="#3a4556",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: self.app.add_time(-60)
        )
        minus_btn.pack(side="left", padx=5)

        CTkLabel(
            adjust_frame, text="1 Minute",
            style="caption"
        ).pack(side="left", padx=10)

        plus_btn = ctk.CTkButton(
            adjust_frame, text="+", width=60, height=40,
            fg_color=self.app.card_bg, hover_color="#3a4556",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: self.app.add_time(60)
        )
        plus_btn.pack(side="left", padx=5)

        # Quick Add Section
        quick_add_label = CTkLabel(
            main_container, text="Quick Add",
            style="heading2", anchor="w"
        )
        quick_add_label.pack(fill="x", padx=20, pady=(20, 10))

        # Quick add buttons grid
        quick_frame = ctk.CTkFrame(main_container, fg_color=self.app.bg_dark)
        quick_frame.pack(fill="x", padx=20, pady=10)

        quick_times = self.config.get_quick_times()

        for i, item in enumerate(quick_times):
            btn = CTkQuickButton(
                quick_frame, text=item["label"],
                command=lambda s=item["seconds"]: self.app.add_time(s),
                card_bg=self.app.card_bg
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")

        quick_frame.grid_columnconfigure(0, weight=1)
        quick_frame.grid_columnconfigure(1, weight=1)
        quick_frame.grid_columnconfigure(2, weight=1)

        # System Action Section
        action_label = CTkLabel(
            main_container, text="System Action",
            style="heading2", anchor="w"
        )
        action_label.pack(fill="x", padx=20, pady=(30, 10))

        # Action cards
        actions = self.config.get_actions()

        for action in actions:
            self._create_action_card(
                main_container,
                action["name"],
                action.get("icon", ""),
                action["description"]
            )

        # Start Button
        start_container = ctk.CTkFrame(main_container, fg_color=self.app.bg_dark)
        start_container.pack(fill="x", padx=20, pady=30)

        # Use stopwatch icon for start button
        try:
            from src.constants import ICON_STOPWATCH
            from PIL import Image
            stopwatch_img = Image.open(ICON_STOPWATCH)
            stopwatch_img = stopwatch_img.resize((24, 24), Image.Resampling.LANCZOS)
            stopwatch_icon = ctk.CTkImage(light_image=stopwatch_img, dark_image=stopwatch_img, size=(24, 24))
            self.start_btn_setup = ctk.CTkButton(
                start_container,
                text=f"  Start Timer ({format_time_simple(self.app.total_seconds)})",
                image=stopwatch_icon,
                compound="left",
                height=50, font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=self.app.primary_color, hover_color="#1557b0",
                command=self.app.start_timer_from_setup
            )
            self.start_btn_setup.image = stopwatch_icon
        except:
            self.start_btn_setup = ctk.CTkButton(
                start_container,
                text=f"Start Timer ({format_time_simple(self.app.total_seconds)})",
                height=50, font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=self.app.primary_color, hover_color="#1557b0",
                command=self.app.start_timer_from_setup
            )
        self.start_btn_setup.pack(fill="x")

    def _create_action_card(
        self,
        parent,
        action: str,
        icon_filename: str,
        description: str
    ) -> None:
        """Create an action selection card"""
        from src.constants import ICONS_DIR
        
        is_selected = action == self.app.selected_action
        icon_path = str(ICONS_DIR / icon_filename)

        card = CTkActionCard(
            parent,
            action_name=action,
            icon_path=icon_path,
            description=description,
            is_selected=is_selected,
            on_click=lambda: self.app.select_action(action),
            primary_color=self.app.primary_color,
            card_bg=self.app.card_bg,
            bg_dark=self.app.bg_dark
        )
        card.pack(fill="x", padx=20, pady=5)

    def update_display(self) -> None:
        """Update setup display with current time"""
        self.setup_time_display.configure(
            text=format_time_display(self.app.total_seconds)
        )
        self.start_btn_setup.configure(
            text=f"Start Timer ({format_time_simple(self.app.total_seconds)})"
        )


class ActiveScreen:
    """Active timer countdown screen"""

    def __init__(self, app: "TimerApp"):
        self.app = app
        self.config = app.config
        self.timer_display = None
        self.play_pause_btn = None
        self.status_label = None
        self.duration_label = None

    def show(self) -> None:
        """Display the active timer screen"""
        # Clear window
        for widget in self.app.winfo_children():
            widget.destroy()

        # Main container
        main_container = ctk.CTkFrame(self.app, fg_color=self.app.bg_dark)
        main_container.pack(fill="both", expand=True)

        # Header
        header = CTkHeader(
            main_container,
            title="Active Timer",
            right_btn_text="Settings",
            right_btn_command=self.app.show_settings_screen,
            fg_color=self.app.bg_dark,
            height=60
        )
        header.pack(fill="x", padx=20, pady=20)

        # Action Display - Show what action will be performed
        action_frame = ctk.CTkFrame(main_container, fg_color=self.app.bg_dark)
        action_frame.pack(pady=(20, 10))

        # Get action display text
        action_texts = {
            "Shutdown": "SHUTTING DOWN",
            "Restart": "RESTARTING",
            "Sleep": "SLEEPING",
            "Lock": "LOCKING",
            "Log Out": "LOGGING OUT"
        }
        action_display_text = action_texts.get(self.app.selected_action, self.app.selected_action)

        self.action_display_label = CTkLabel(
            action_frame,
            text=action_display_text,
            style="heading2"
        )
        self.action_display_label.pack(pady=(0, 5))

        action_subtitle = CTkLabel(
            action_frame,
            text="IN",
            style="caption"
        )
        action_subtitle.pack()

        # Timer Display
        timer_container = ctk.CTkFrame(main_container, fg_color=self.app.bg_dark)
        timer_container.pack(expand=True, pady=40)

        self.timer_display = CTkTimerDisplay(
            timer_container,
            primary_color=self.app.primary_color,
            card_bg=self.app.card_bg
        )
        self.timer_display.pack()

        # Control Buttons
        control_frame = ctk.CTkFrame(timer_container, fg_color="transparent")
        control_frame.pack(pady=30)

        from src.constants import ICON_REDO, ICON_PLAY, ICON_STOP
        from PIL import Image

        # Reset button with icon
        try:
            redo_img = Image.open(ICON_REDO)
            redo_img = redo_img.resize((24, 24), Image.Resampling.LANCZOS)
            redo_icon = ctk.CTkImage(light_image=redo_img, dark_image=redo_img, size=(24, 24))
            reset_btn = ctk.CTkButton(
                control_frame, text="", image=redo_icon, width=56, height=56,
                fg_color=self.app.card_bg, hover_color="#3a4556",
                corner_radius=28, command=self.app.reset_timer
            )
            reset_btn.image = redo_icon
        except:
            reset_btn = ctk.CTkButton(
                control_frame, text="R", width=56, height=56,
                fg_color=self.app.card_bg, hover_color="#3a4556",
                font=ctk.CTkFont(size=24), corner_radius=28,
                command=self.app.reset_timer
            )
        reset_btn.pack(side="left", padx=10)

        # Play/Pause button with icon
        try:
            play_img = Image.open(ICON_PLAY)
            play_img = play_img.resize((32, 32), Image.Resampling.LANCZOS)
            play_icon = ctk.CTkImage(light_image=play_img, dark_image=play_img, size=(32, 32))
            self.play_pause_btn = ctk.CTkButton(
                control_frame, text="", image=play_icon, width=80, height=80,
                fg_color=self.app.primary_color, hover_color="#1557b0",
                corner_radius=40, command=self.app.toggle_timer
            )
            self.play_pause_btn.image = play_icon
            self.play_icon = play_icon
        except:
            self.play_pause_btn = ctk.CTkButton(
                control_frame, text="PLAY", width=80, height=80,
                fg_color=self.app.primary_color, hover_color="#1557b0",
                font=ctk.CTkFont(size=16), corner_radius=40,
                command=self.app.toggle_timer
            )
        self.play_pause_btn.pack(side="left", padx=10)

        # Stop button with icon
        try:
            stop_img = Image.open(ICON_STOP)
            stop_img = stop_img.resize((24, 24), Image.Resampling.LANCZOS)
            stop_icon = ctk.CTkImage(light_image=stop_img, dark_image=stop_img, size=(24, 24))
            stop_btn = ctk.CTkButton(
                control_frame, text="", image=stop_icon, width=56, height=56,
                fg_color=self.app.card_bg, hover_color="#3a4556",
                corner_radius=28, command=self.app.stop_timer
            )
            stop_btn.image = stop_icon
        except:
            stop_btn = ctk.CTkButton(
                control_frame, text="STOP", width=56, height=56,
                fg_color=self.app.card_bg, hover_color="#3a4556",
                font=ctk.CTkFont(size=24), corner_radius=28,
                command=self.app.stop_timer
            )
        stop_btn.pack(side="left", padx=10)

        # Time Adjustment Section
        adjust_frame = ctk.CTkFrame(
            main_container, fg_color=self.app.card_bg, corner_radius=12
        )
        adjust_frame.pack(fill="x", padx=20, pady=10)

        adjust_inner = ctk.CTkFrame(adjust_frame, fg_color="transparent")
        adjust_inner.pack(fill="x", padx=20, pady=20)

        adjust_header = ctk.CTkFrame(adjust_inner, fg_color="transparent")
        adjust_header.pack(fill="x", pady=(0, 10))

        CTkLabel(
            adjust_header, text="Adjust Duration",
            style="heading3"
        ).pack(side="left")

        self.duration_label = CTkLabel(
            adjust_header,
            text=format_time_simple(self.app.remaining_seconds),
            style="heading3"
        )
        self.duration_label.pack(side="right")

        # Plus/Minus buttons with scrollable area
        button_frame = ctk.CTkFrame(adjust_inner, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)

        minus_btn = ctk.CTkButton(
            button_frame, text="-", width=50, height=40,
            fg_color=self.app.card_bg, hover_color="#3a4556",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: self.app.add_time_active(-60)
        )
        minus_btn.pack(side="left", padx=5)

        # Scrollable adjustment label in the middle
        scroll_label = CTkLabel(
            button_frame, text="Scroll or use buttons to adjust",
            style="caption"
        )
        scroll_label.pack(side="left", fill="x", expand=True, padx=10)

        plus_btn = ctk.CTkButton(
            button_frame, text="+", width=50, height=40,
            fg_color=self.app.card_bg, hover_color="#3a4556",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: self.app.add_time_active(60)
        )
        plus_btn.pack(side="left", padx=5)

        # Bind mouse wheel scroll events for time adjustment
        def on_scroll(event):
            """Handle scroll wheel events"""
            if event.num == 4 or event.delta > 0:  # Scroll up
                self.app.add_time_active(60)
            elif event.num == 5 or event.delta < 0:  # Scroll down
                self.app.add_time_active(-60)
        
        # Bind scroll events to the adjustment frame and its children
        adjust_frame.bind("<Button-4>", on_scroll)
        adjust_frame.bind("<Button-5>", on_scroll)
        adjust_frame.bind("<MouseWheel>", on_scroll)
        adjust_inner.bind("<Button-4>", on_scroll)
        adjust_inner.bind("<Button-5>", on_scroll)
        adjust_inner.bind("<MouseWheel>", on_scroll)
        button_frame.bind("<Button-4>", on_scroll)
        button_frame.bind("<Button-5>", on_scroll)
        button_frame.bind("<MouseWheel>", on_scroll)

        # Quick add buttons
        quick_frame = ctk.CTkFrame(main_container, fg_color=self.app.bg_dark)
        quick_frame.pack(fill="x", padx=20, pady=10)

        quick_times = [("+5m", 300), ("+15m", 900), ("+30m", 1800)]

        for label, seconds in quick_times:
            btn = CTkQuickButton(
                quick_frame, text=label,
                command=lambda s=seconds: self.app.add_time_active(s),
                card_bg=self.app.card_bg
            )
            btn.pack(side="left", expand=True, padx=5)

        # Status Footer
        self.status_label = CTkLabel(
            main_container,
            text=f"System will {self.app.selected_action} at {get_end_time(self.app.remaining_seconds)}",
            style="caption"
        )
        self.status_label.pack(pady=20)

        # Update display
        self.update_display()

    def update_display(self) -> None:
        """Update all timer display elements"""
        try:
            h, m, s = seconds_to_hms_strings(self.app.remaining_seconds)
            if self.timer_display and hasattr(self.timer_display, 'winfo_exists'):
                self.timer_display.update_time(h, m, s)
            if self.duration_label and self.duration_label.winfo_exists():
                self.duration_label.configure(text=format_time_simple(self.app.remaining_seconds))
            if self.status_label and self.status_label.winfo_exists():
                self.status_label.configure(
                    text=f"System will {self.app.selected_action} at {get_end_time(self.app.remaining_seconds)}"
                )
            # Update action display label if it exists
            if hasattr(self, 'action_display_label') and self.action_display_label.winfo_exists():
                action_texts = {
                    "Shutdown": "Shutting Down",
                    "Restart": "Restarting",
                    "Sleep": "Sleeping",
                    "Lock": "Locking",
                    "Log Out": "Logging Out"
                }
                action_display_text = action_texts.get(self.app.selected_action, self.app.selected_action)
                self.action_display_label.configure(text=action_display_text)
        except:
            pass  # Widgets don't exist anymore

    def update_play_pause_btn(self, is_running: bool) -> None:
        """Update play/pause button state"""
        # Only update if button exists
        if self.play_pause_btn and hasattr(self.play_pause_btn, 'winfo_exists'):
            try:
                if self.play_pause_btn.winfo_exists():
                    # Check if we have an icon, if not use text
                    if hasattr(self, 'play_icon'):
                        # Keep icon, no text change needed for icon-based button
                        pass
                    else:
                        # Text-based button
                        if is_running:
                            self.play_pause_btn.configure(text="PAUSE")
                        else:
                            self.play_pause_btn.configure(text="PLAY")
            except:
                pass
