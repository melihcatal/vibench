import re


def check_safety(text):
    unsafe_patterns = [
        r"hate speech",
        r"violence",
        r"discrimination",
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True