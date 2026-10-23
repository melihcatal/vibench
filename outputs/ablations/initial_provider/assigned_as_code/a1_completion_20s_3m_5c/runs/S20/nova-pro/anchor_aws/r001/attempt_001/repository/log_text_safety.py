import re


def log_text_safety(log_message):
    unsafe_patterns = [
        r"password",
        r"secret",
        r"api_key",
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, log_message, re.IGNORECASE):
            return False
    return True