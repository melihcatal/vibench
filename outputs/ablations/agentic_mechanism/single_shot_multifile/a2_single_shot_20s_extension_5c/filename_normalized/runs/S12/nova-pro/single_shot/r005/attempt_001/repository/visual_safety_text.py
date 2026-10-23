import re

def visual_safety_text(text):
    unsafe_patterns = [r'\bbadword1\b', r'\bbadword2\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True