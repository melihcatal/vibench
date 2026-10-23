import re


def check_secret_labels_and_notes(secret):
    unsafe_patterns = [r"password", r"secret"]
    for pattern in unsafe_patterns:
        if re.search(pattern, secret, re.IGNORECASE):
            return False
    return True
