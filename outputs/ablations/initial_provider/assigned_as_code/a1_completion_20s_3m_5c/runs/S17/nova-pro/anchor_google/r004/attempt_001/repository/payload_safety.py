import re

def payload_safety(plaintext):
    if re.search(r'\bunsafe\b', plaintext, re.IGNORECASE):
        return {"is_safe": False}
    return {"is_safe": True}