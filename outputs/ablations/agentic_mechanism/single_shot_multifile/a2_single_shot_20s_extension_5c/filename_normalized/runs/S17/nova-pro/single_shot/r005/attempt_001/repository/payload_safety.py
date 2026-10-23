import re

def check_payload_safety(plaintext):
    unsafe_patterns = [r'malware', r'virus']
    for pattern in unsafe_patterns:
        if re.search(pattern, plaintext):
            return False
    return True