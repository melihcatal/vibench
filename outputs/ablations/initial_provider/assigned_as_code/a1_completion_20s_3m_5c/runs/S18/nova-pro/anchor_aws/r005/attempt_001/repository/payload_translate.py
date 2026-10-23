import re

def check_message_safety(message):
    unsafe_patterns = [r'<script>', r'<iframe>']
    for pattern in unsafe_patterns:
        if re.search(pattern, message):
            return False
    return True