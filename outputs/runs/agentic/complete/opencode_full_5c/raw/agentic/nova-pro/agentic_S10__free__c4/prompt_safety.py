import re


def check_unsafe_content(text):
    unsafe_patterns = [r"\b(hate|violence|discrimination)\b"]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
