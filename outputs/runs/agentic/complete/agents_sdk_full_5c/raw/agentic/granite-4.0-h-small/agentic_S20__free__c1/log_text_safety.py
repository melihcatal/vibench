import json
import re
from observability_models import LogEvent

# Simple profanity/unsafe content checker
UNSAFE_PATTERN = re.compile(r"(?:hate|bomb|kill|weapon|drugs|suicide)", re.I)

def log_text_safety(log_event: LogEvent) -> bool:
    """Check whether a log event's message contains unsafe content.

    Args:
        log_event (LogEvent): Normalized log entry.

    Returns:
        bool: True if safe, False if unsafe text is detected.
    """
    text = log_event.get('message', '')
    return not UNSAFE_PATTERN.search(text)
