import re


# Check Secret Labels and Notes for Unsafe Text
def secret_label_safety(text):
    unsafe_patterns = [r"password", r"secret", r"key"]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True
