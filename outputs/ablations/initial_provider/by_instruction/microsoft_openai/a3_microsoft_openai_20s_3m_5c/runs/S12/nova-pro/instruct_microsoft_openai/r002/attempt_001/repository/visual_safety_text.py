import re

def visual_safety_text(text):
    unsafe_patterns = [r'\bunsafe\b', r'\bpolicy-sensitive\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False