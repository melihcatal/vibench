import re


def check_message_safety(payload):
    unsafe_patterns = [re.compile(pattern) for pattern in ['malicious', 'dangerous']]
    for pattern in unsafe_patterns:
        if pattern.search(payload):
            return False
    return True