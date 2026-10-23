import re


def payload_safety(decrypted_text):
    unsafe_patterns = [r'<script>', r'<iframe>', r'<object>']
    for pattern in unsafe_patterns:
        if re.search(pattern, decrypted_text):
            return False
    return True