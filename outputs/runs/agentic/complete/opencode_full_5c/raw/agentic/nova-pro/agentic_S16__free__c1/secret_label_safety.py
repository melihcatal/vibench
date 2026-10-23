import re


def check_secret_labels(secret_labels):
    unsafe_patterns = ["password", "secret", "key"]
    for label in secret_labels:
        if any(re.search(pattern, label) for pattern in unsafe_patterns):
            return False
    return True
