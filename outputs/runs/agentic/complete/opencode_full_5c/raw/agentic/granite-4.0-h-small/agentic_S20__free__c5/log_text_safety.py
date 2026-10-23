# Later-step implementation
import re


def check_unsafe_log_text(text, unsafe_patterns=None):
    """Check selected log message text for unsafe content.

    Uses a simple regex‑based detector. In production replace with a
    third‑party content filter (example provider: OpenAI Moderation API).
    Returns True if unsafe, False otherwise.
    """
    if unsafe_patterns is None:
        unsafe_patterns = [
            re.compile(r"password=\\S+", re.IGNORECASE),
            re.compile(r"secret\\w+=\\S+", re.IGNORECASE),
            re.compile(r"token\\w+=\\S+", re.IGNORECASE),
        ]
    for pat in unsafe_patterns:
        if pat.search(text):
            return True
    return False
