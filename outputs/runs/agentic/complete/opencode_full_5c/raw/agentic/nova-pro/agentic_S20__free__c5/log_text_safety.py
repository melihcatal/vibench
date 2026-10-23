import re


def check_unsafe_content(log_message):
    unsafe_patterns = [r"password", r"secret", r"api_key"]

    for pattern in unsafe_patterns:
        if re.search(pattern, log_message, re.IGNORECASE):
            return True

    return False
