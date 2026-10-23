import re

def check_unsafe_text(text):
    unsafe_patterns = [r'pattern1', r'pattern2']
    for pattern in unsafe_patterns:
        if re.search(pattern, text):
            return True
    return False