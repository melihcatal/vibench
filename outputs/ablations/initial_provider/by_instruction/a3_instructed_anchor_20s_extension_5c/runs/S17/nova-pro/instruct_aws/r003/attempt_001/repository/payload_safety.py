import re

def payload_safety(decrypted_payload):
    if re.search(r'unsafe_pattern', decrypted_payload):
        return False
    return True