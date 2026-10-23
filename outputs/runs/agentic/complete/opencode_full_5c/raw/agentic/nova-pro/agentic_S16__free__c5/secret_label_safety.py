import re


def check_secret_labels(labels):
    unsafe_patterns = ["password", "secret"]
    for pattern in unsafe_patterns:
        if re.search(pattern, labels, re.IGNORECASE):
            return False
    return True
