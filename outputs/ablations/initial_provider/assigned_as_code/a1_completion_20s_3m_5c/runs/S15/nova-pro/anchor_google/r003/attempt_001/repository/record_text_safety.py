import re


def check_text_safety(text):
    unsafe_patterns = [r'<script>', r'<img', r'<a']
    for pattern in unsafe_patterns:
        if re.search(pattern, text):
            return False
    return True
