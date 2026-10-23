import re


def check_secret_label_safety(label):
    unsafe_patterns = [r'password', r'secret', r'key']
    for pattern in unsafe_patterns:
        if re.search(pattern, label, re.IGNORECASE):
            return False
    return True