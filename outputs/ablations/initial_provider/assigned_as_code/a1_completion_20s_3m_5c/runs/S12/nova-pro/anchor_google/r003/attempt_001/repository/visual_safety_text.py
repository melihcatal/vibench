import re

def check_unsafe_text(text):
    unsafe_patterns = [
        r'\b(badword1|badword2)\b',
        r'\b(badword3|badword4)\b',
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False