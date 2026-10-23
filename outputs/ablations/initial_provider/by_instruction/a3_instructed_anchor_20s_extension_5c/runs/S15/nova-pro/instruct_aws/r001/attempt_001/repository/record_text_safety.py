import re

def check_safety(text):
    unsafe_patterns = [r'<.*?>', r'javascript:', r'vbscript:']
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True