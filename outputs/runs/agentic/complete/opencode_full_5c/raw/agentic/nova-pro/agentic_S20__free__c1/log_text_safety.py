import re


def check_log_text_safety(log_text):
    unsafe_patterns = [r"password", r"secret"]
    for pattern in unsafe_patterns:
        if re.search(pattern, log_text, re.IGNORECASE):
            return False
    return True
