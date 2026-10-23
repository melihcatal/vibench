import re

def check_payload_safety(plaintext):
    unsafe_patterns = [r'malware', r'virus', r'ransomware']
    for pattern in unsafe_patterns:
        if re.search(pattern, plaintext, re.IGNORECASE):
            return False
    return True
