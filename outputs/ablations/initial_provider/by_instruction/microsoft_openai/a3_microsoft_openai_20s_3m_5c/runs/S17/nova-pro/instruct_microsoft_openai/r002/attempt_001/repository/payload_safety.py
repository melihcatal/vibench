import re

def check_payload_safety(decrypted_text):
    unsafe_patterns = [r'password', r'secret']
    for pattern in unsafe_patterns:
        if re.search(pattern, decrypted_text, re.IGNORECASE):
            return False
    return True
