import re

def check_unsafe_content(text):
    unsafe_patterns = [r'\b(porn|sex|nudity)\b', r'\b(hate|violence)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False