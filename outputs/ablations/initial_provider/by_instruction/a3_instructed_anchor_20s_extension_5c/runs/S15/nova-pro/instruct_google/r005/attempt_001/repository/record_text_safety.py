import re

def check_text_safety(text):
    unsafe_patterns = [r'<script>', r'<iframe>', r'<object>']
    for pattern in unsafe_patterns:
        if re.search(pattern, text):
            return False
    return True