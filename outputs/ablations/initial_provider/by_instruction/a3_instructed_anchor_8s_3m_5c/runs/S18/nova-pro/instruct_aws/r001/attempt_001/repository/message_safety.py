import re

def check_unsafe_content(message):
    unsafe_patterns = [r'password', r'secret']
    for pattern in unsafe_patterns:
        if re.search(pattern, message):
            return True
    return False