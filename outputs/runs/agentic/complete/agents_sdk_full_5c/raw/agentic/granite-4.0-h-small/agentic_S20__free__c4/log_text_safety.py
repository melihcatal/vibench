import re

def is_unsafe_text(text: str) -> bool:
    """
    Very simple safety check for log messages.
    Returns True if the text contains URLs or email addresses that could be unsafe.
    """
    url_pattern = re.compile(r\"https?://[^\\s]+\")
    email_pattern = re.compile(r\"[\\w.%+-]+@[\\w.-]+\\.[a-zA-Z]{2,}\")
    return bool(url_pattern.search(text) or email_pattern.search(text))