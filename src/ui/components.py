"""
Reusable UI components for CustomTkinter
"""
import customtkinter as ctk
from typing import Callable, Optional
from PIL import Image


class CTkHeader(ctk.CTkFrame):
    """Reusable header frame with title and action buttons"""

    def __init__(
        self,
        parent,
        title: str = "",
        left_btn_text: str = None,
        left_btn_command: Callable = None,
        right_btn_text: str = None,
        right_btn_command: Callable = None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        
        # Left button - use icon if text is "Back"
        if left_btn_text and left_btn_command:
            if left_btn_text.lower() == "back":
                # Use back icon
                try:
                    from src.constants import ICON_BACK
                    back_img = Image.open(ICON_BACK)
                    back_img = back_img.resize((20, 20), Image.Resampling.LANCZOS)
                    back_icon = ctk.CTkImage(light_image=back_img, dark_image=back_img, size=(20, 20))
                    self.left_btn = ctk.CTkButton(
                        self, text="", image=back_icon, width=40, height=40,
                        fg_color="transparent", hover_color=kwargs.get("hover_color", "#2d3748"),
                        command=left_btn_command
                    )
                    self.left_btn.image = back_icon
                except:
                    # Fallback to text
                    self.left_btn = ctk.CTkButton(
                        self, text=left_btn_text, width=40, height=40,
                        fg_color="transparent", hover_color=kwargs.get("hover_color", "#2d3748"),
                        font=ctk.CTkFont(size=14), command=left_btn_command
                    )
            else:
                self.left_btn = ctk.CTkButton(
                    self, text=left_btn_text, width=40, height=40,
                    fg_color="transparent", hover_color=kwargs.get("hover_color", "#2d3748"),
                    font=ctk.CTkFont(size=14), command=left_btn_command
                )
            self.left_btn.pack(side="left", padx=10)
        
        # Title
        if title:
            self.title_label = ctk.CTkLabel(
                self, text=title,
                font=ctk.CTkFont(size=18, weight="bold")
            )
            self.title_label.pack(side="left", expand=True, padx=10)
        
        # Right button - use icon if text is "Settings"
        if right_btn_text and right_btn_command:
            if right_btn_text.lower() == "settings":
                # Use settings icon
                try:
                    from src.constants import ICON_SETTINGS
                    settings_img = Image.open(ICON_SETTINGS)
                    settings_img = settings_img.resize((20, 20), Image.Resampling.LANCZOS)
                    settings_icon = ctk.CTkImage(light_image=settings_img, dark_image=settings_img, size=(20, 20))
                    self.right_btn = ctk.CTkButton(
                        self, text="", image=settings_icon, width=40, height=40,
                        fg_color="transparent", hover_color=kwargs.get("hover_color", "#2d3748"),
                        command=right_btn_command
                    )
                    self.right_btn.image = settings_icon
                except:
                    # Fallback to text
                    self.right_btn = ctk.CTkButton(
                        self, text=right_btn_text, width=40, height=40,
                        fg_color="transparent", hover_color=kwargs.get("hover_color", "#2d3748"),
                        font=ctk.CTkFont(size=14), command=right_btn_command
                    )
            else:
                self.right_btn = ctk.CTkButton(
                    self, text=right_btn_text, width=40, height=40,
                    fg_color="transparent", hover_color=kwargs.get("hover_color", "#2d3748"),
                    font=ctk.CTkFont(size=14), command=right_btn_command
                )
            self.right_btn.pack(side="right", padx=10)


class CTkCard(ctk.CTkFrame):
    """Card component with optional selection state"""

    def __init__(
        self,
        parent,
        is_selected: bool = False,
        on_click: Callable = None,
        **kwargs
    ):
        primary_color = kwargs.pop("primary_color", "#1973f0")
        card_bg = kwargs.pop("card_bg", "#1c2633")
        
        if is_selected:
            super().__init__(
                parent, fg_color="#1a3a6b", corner_radius=12,
                border_width=2, border_color=primary_color, **kwargs
            )
        else:
            super().__init__(
                parent, fg_color=card_bg, corner_radius=12,
                border_width=0, **kwargs
            )
        
        self.is_selected = is_selected
        self.primary_color = primary_color
        self.on_click = on_click
        
        if on_click:
            self.bind("<Button-1>", lambda e: on_click())

    def set_selected(self, selected: bool) -> None:
        """Update selection state"""
        self.is_selected = selected
        if selected:
            self.configure(
                fg_color="#1a3a6b", border_width=2,
                border_color=self.primary_color
            )
        else:
            self.configure(fg_color="#1c2633", border_width=0)


class CTkActionCard(ctk.CTkFrame):
    """Action selection card with icon, title, and description"""

    def __init__(
        self,
        parent,
        action_name: str,
        icon_path: str,
        description: str,
        is_selected: bool = False,
        on_click: Callable = None,
        **kwargs
    ):
        primary_color = kwargs.pop("primary_color", "#1973f0")
        card_bg = kwargs.pop("card_bg", "#1c2633")
        bg_dark = kwargs.pop("bg_dark", "#101822")
        
        if is_selected:
            super().__init__(
                parent, fg_color="#1a3a6b", corner_radius=12,
                border_width=2, border_color=primary_color
            )
        else:
            super().__init__(
                parent, fg_color=card_bg, corner_radius=12,
                border_width=0
            )
        
        self.is_selected = is_selected
        self.primary_color = primary_color
        self.card_bg = card_bg
        self.on_click = on_click
        self.icon_label = None
        self.check_label = None
        
        self.bind("<Button-1>", lambda e: on_click() if on_click else None)
        
        inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        inner_frame.pack(fill="x", padx=15, pady=15)
        inner_frame.bind("<Button-1>", lambda e: on_click() if on_click else None)
        
        # Icon
        try:
            img = Image.open(icon_path)
            img = img.resize((40, 40), Image.Resampling.LANCZOS)
            icon_image = ctk.CTkImage(light_image=img, size=(40, 40))
            self.icon_label = ctk.CTkLabel(
                inner_frame, image=icon_image, text="",
                fg_color=primary_color if is_selected else "#2d3748",
                width=40, height=40, corner_radius=8
            )
            self.icon_label.image = icon_image
            self.icon_label.pack(side="left", padx=(0, 15))
            self.icon_label.bind("<Button-1>", lambda e: on_click() if on_click else None)
        except Exception:
            pass  # Icon loading failed, continue without it
        
        # Text frame
        text_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        text_frame.bind("<Button-1>", lambda e: on_click() if on_click else None)
        
        # Title
        title_label = ctk.CTkLabel(
            text_frame, text=action_name,
            font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
        )
        title_label.pack(fill="x")
        title_label.bind("<Button-1>", lambda e: on_click() if on_click else None)
        
        # Description
        desc_label = ctk.CTkLabel(
            text_frame, text=description,
            font=ctk.CTkFont(size=11), text_color="#9ca8ba", anchor="w"
        )
        desc_label.pack(fill="x")
        desc_label.bind("<Button-1>", lambda e: on_click() if on_click else None)
        
        # Checkmark icon
        if is_selected:
            try:
                from src.constants import ICON_CHECK
                check_img = Image.open(ICON_CHECK)
                check_img = check_img.resize((20, 20), Image.Resampling.LANCZOS)
                check_icon = ctk.CTkImage(light_image=check_img, dark_image=check_img, size=(20, 20))
                self.check_label = ctk.CTkLabel(
                    inner_frame, text="", image=check_icon
                )
                self.check_label.image = check_icon
                self.check_label.pack(side="right")
                self.check_label.bind("<Button-1>", lambda e: on_click() if on_click else None)
            except Exception:
                # Fallback to text checkmark
                self.check_label = ctk.CTkLabel(
                    inner_frame, text="✓",
                    font=ctk.CTkFont(size=20), text_color=primary_color
                )
                self.check_label.pack(side="right")
                self.check_label.bind("<Button-1>", lambda e: on_click() if on_click else None)

    def set_selected(self, selected: bool) -> None:
        """Update selection state"""
        if self.is_selected == selected:
            return  # No change needed
            
        self.is_selected = selected
        if selected:
            self.configure(
                fg_color="#1a3a6b", border_width=2,
                border_color=self.primary_color
            )
            # Update icon background
            if self.icon_label:
                self.icon_label.configure(fg_color=self.primary_color)
            # Add checkmark icon if not present
            if not self.check_label or not self.check_label.winfo_exists():
                # Find the inner frame (parent of icon_label)
                if self.icon_label:
                    inner_frame = self.icon_label.master
                    try:
                        from src.constants import ICON_CHECK
                        check_img = Image.open(ICON_CHECK)
                        check_img = check_img.resize((20, 20), Image.Resampling.LANCZOS)
                        check_icon = ctk.CTkImage(light_image=check_img, dark_image=check_img, size=(20, 20))
                        self.check_label = ctk.CTkLabel(
                            inner_frame, text="", image=check_icon
                        )
                        self.check_label.image = check_icon
                        self.check_label.pack(side="right")
                        self.check_label.bind("<Button-1>", lambda e: self.on_click() if self.on_click else None)
                    except Exception:
                        # Fallback to text checkmark
                        self.check_label = ctk.CTkLabel(
                            inner_frame, text="✓",
                            font=ctk.CTkFont(size=20), text_color=self.primary_color
                        )
                        self.check_label.pack(side="right")
                        self.check_label.bind("<Button-1>", lambda e: self.on_click() if self.on_click else None)
        else:
            self.configure(fg_color=self.card_bg, border_width=0)
            # Update icon background
            if self.icon_label:
                self.icon_label.configure(fg_color="#2d3748")
            # Remove checkmark
            if self.check_label and self.check_label.winfo_exists():
                self.check_label.destroy()
                self.check_label = None


class CTkQuickButton(ctk.CTkButton):
    """Quick action button with consistent styling"""

    def __init__(
        self,
        parent,
        text: str = "",
        command: Callable = None,
        **kwargs
    ):
        card_bg = kwargs.pop("card_bg", "#1c2633")
        hover_color = kwargs.pop("hover_color", "#3a4556")
        
        super().__init__(
            parent, text=text, height=45,
            fg_color=card_bg, hover_color=hover_color,
            command=command, **kwargs
        )


class CTkTimerDisplay(ctk.CTkFrame):
    """Timer display with hours, minutes, and seconds"""

    def __init__(
        self,
        parent,
        hours: str = "00",
        minutes: str = "15",
        seconds: str = "00",
        **kwargs
    ):
        primary_color = kwargs.pop("primary_color", "#1973f0")
        card_bg = kwargs.pop("card_bg", "#1c2633")
        
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        time_frame = ctk.CTkFrame(self, fg_color="transparent")
        time_frame.pack()
        
        # Hours
        hours_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        hours_frame.pack(side="left", padx=5)
        
        self.hours_label = ctk.CTkLabel(
            hours_frame, text=hours,
            font=ctk.CTkFont(size=48, weight="bold"),
            fg_color=card_bg, width=90, height=90, corner_radius=12
        )
        self.hours_label.pack()
        
        ctk.CTkLabel(
            hours_frame, text="HOURS",
            font=ctk.CTkFont(size=8), text_color="#9ca8ba"
        ).pack(pady=(5, 0))
        
        # Separator
        ctk.CTkLabel(
            time_frame, text=":",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color=primary_color
        ).pack(side="left", padx=5)
        
        # Minutes
        minutes_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        minutes_frame.pack(side="left", padx=5)
        
        self.minutes_label = ctk.CTkLabel(
            minutes_frame, text=minutes,
            font=ctk.CTkFont(size=48, weight="bold"),
            fg_color=card_bg, width=90, height=90, corner_radius=12
        )
        self.minutes_label.pack()
        
        ctk.CTkLabel(
            minutes_frame, text="MINUTES",
            font=ctk.CTkFont(size=8), text_color="#9ca8ba"
        ).pack(pady=(5, 0))
        
        # Separator
        ctk.CTkLabel(
            time_frame, text=":",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color=primary_color
        ).pack(side="left", padx=5)
        
        # Seconds
        seconds_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        seconds_frame.pack(side="left", padx=5)
        
        self.seconds_label = ctk.CTkLabel(
            seconds_frame, text=seconds,
            font=ctk.CTkFont(size=48, weight="bold"),
            fg_color=card_bg, width=90, height=90, corner_radius=12
        )
        self.seconds_label.pack()
        
        ctk.CTkLabel(
            seconds_frame, text="SECONDS",
            font=ctk.CTkFont(size=8), text_color="#9ca8ba"
        ).pack(pady=(5, 0))

    def update_time(self, hours: str, minutes: str, seconds: str) -> None:
        """Update displayed time"""
        try:
            if self.hours_label.winfo_exists():
                self.hours_label.configure(text=hours)
            if self.minutes_label.winfo_exists():
                self.minutes_label.configure(text=minutes)
            if self.seconds_label.winfo_exists():
                self.seconds_label.configure(text=seconds)
        except:
            pass  # Widget doesn't exist anymore


class CTkIconButton(ctk.CTkButton):
    """Button with icon image"""

    def __init__(
        self,
        parent,
        icon_path: Optional[str] = None,
        text: str = "",
        command: Callable = None,
        **kwargs
    ):
        super().__init__(parent, text=text, command=command, **kwargs)
        
        if icon_path:
            try:
                img = Image.open(icon_path)
                img = img.resize((24, 24), Image.Resampling.LANCZOS)
                icon_image = ctk.CTkImage(light_image=img, size=(24, 24))
                self.configure(image=icon_image)
                self.image = icon_image
            except Exception:
                pass  # Icon loading failed, use text only


class CTkScrollableSection(ctk.CTkScrollableFrame):
    """Scrollable frame with padding and styling"""

    def __init__(self, parent, **kwargs):
        # Use fg_color if provided, otherwise use bg_color, otherwise default
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = kwargs.pop("bg_color", "#101822")
        else:
            kwargs.pop("bg_color", None)  # Remove bg_color if fg_color is set
        super().__init__(parent, **kwargs)


class CTkLabel(ctk.CTkLabel):
    """Enhanced label with common text styles"""

    def __init__(self, parent, style: str = "body", **kwargs):
        styles = {
            "heading1": {"font": ctk.CTkFont(size=20, weight="bold")},
            "heading2": {"font": ctk.CTkFont(size=16, weight="bold")},
            "heading3": {"font": ctk.CTkFont(size=14, weight="bold")},
            "body": {"font": ctk.CTkFont(size=12)},
            "caption": {"font": ctk.CTkFont(size=10), "text_color": "#9ca8ba"},
            "code": {"font": ctk.CTkFont(family="Courier", size=11)},
        }
        
        style_props = styles.get(style, {})
        kwargs.update(style_props)
        super().__init__(parent, **kwargs)
