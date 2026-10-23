import re

def check_unsafe_content(text):
    unsafe_patterns = [r'badword1', r'badword2']
    for pattern in unsafe_patterns:
        if re.search(pattern, text):
            return True
    return False