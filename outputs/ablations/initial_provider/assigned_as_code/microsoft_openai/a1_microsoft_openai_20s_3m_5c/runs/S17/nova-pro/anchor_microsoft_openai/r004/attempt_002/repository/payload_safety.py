import re

def payload_safety(plaintext):
    if re.search(r'unsafe', plaintext):
        return False
    return True