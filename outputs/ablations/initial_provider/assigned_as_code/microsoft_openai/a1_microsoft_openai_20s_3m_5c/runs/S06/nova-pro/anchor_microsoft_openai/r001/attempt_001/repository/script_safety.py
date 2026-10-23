import os
import re

def check_safety(text):
    unsafe_patterns = [
        r'\b(hate|violence|discrimination)\b',
        r'\b(kill|murder|assault)\b',
        r'\b(abuse|harassment)\b',
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True
