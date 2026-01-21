"""
Utility functions for time formatting and manipulation
"""
from datetime import datetime, timedelta


def format_time_display(seconds: int) -> str:
    """Format time for large display (HH:MM:SS)"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_time_simple(seconds: int) -> str:
    """Format time for simple display (MM:SS or HH:MM)"""
    if seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"


def get_time_components(seconds: int) -> tuple:
    """Get hours, minutes, seconds as integers"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return hours, minutes, secs


def seconds_to_hms_strings(seconds: int) -> tuple:
    """Get formatted HH, MM, SS strings"""
    hours, minutes, secs = get_time_components(seconds)
    return f"{hours:02d}", f"{minutes:02d}", f"{secs:02d}"


def get_end_time(remaining_seconds: int) -> str:
    """Calculate and format the end time"""
    end_time = datetime.now() + timedelta(seconds=remaining_seconds)
    return end_time.strftime("%I:%M %p")


def is_valid_duration(seconds: int, min_val: int = 60, max_val: int = 86400) -> bool:
    """Check if duration is within valid range"""
    return min_val <= seconds <= max_val
