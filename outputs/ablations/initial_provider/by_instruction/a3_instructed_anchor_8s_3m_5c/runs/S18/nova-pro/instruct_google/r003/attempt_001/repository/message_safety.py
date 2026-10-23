import re

def check_safety(text):
    unsafe_patterns = [r'badword1', r'badword2']
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True