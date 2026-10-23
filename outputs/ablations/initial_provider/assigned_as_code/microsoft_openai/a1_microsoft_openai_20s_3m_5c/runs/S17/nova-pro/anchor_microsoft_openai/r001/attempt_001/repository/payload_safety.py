import re

def payload_safety(plaintext):
    unsafe_patterns = [r'<script>', r'<iframe>', r'<object>']
    for pattern in unsafe_patterns:
        if re.search(pattern, plaintext):
            return False
    return True