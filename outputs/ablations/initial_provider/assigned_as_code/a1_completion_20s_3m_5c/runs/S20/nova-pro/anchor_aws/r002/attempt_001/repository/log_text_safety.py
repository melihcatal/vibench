import re


def check_log_message_safety(message):
    unsafe_patterns = [
        r"password", r"secret", r"token", r"api_key", r"access_key"
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return False
    return True