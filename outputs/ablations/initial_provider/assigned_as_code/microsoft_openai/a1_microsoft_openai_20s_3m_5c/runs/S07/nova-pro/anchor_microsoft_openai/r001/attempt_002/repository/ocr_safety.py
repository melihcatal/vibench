import re

def check_unsafe_content(text):
    unsafe_patterns = [r'\b(adult|porn|sex)\b', r'\b(hate|racism|discrimination)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False