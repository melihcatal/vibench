import re


def message_safety(message):
    unsafe_patterns = [r"password", r"secret"]
    for pattern in unsafe_patterns:
        if re.search(pattern, message):
            return False
    return True
