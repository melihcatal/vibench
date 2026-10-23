import re

def check_payload_safety(plaintext):
    if re.search(r'unsafe_pattern', plaintext):
        return False
    return True