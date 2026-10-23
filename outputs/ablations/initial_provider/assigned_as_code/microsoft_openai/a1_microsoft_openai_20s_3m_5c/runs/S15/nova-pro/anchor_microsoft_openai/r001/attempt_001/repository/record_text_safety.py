import re

def check_unsafe_content(fields):
    unsafe_patterns = [r'<script>', r'<img', r'<a']
    for field in fields:
        if any(re.search(pattern, field) for pattern in unsafe_patterns):
            return True
    return False