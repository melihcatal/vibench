import re

def check_safety(message):
    unsafe_patterns = [r"badword1", r"badword2"]
    for pattern in unsafe_patterns:
        if re.search(pattern, message):
            return False
    return True