import re


def payload_safety(plaintext):
    unsafe_patterns = [
        re.compile(r'<script.*?>.*?</script>', re.IGNORECASE),
        re.compile(r'<.*?javascript:.*?>', re.IGNORECASE),
        re.compile(r'<.*?vbscript:.*?>', re.IGNORECASE),
        re.compile(r'<.*?expression.*?>', re.IGNORECASE)
    ]
    for pattern in unsafe_patterns:
        if pattern.search(plaintext):
            return False
    return True