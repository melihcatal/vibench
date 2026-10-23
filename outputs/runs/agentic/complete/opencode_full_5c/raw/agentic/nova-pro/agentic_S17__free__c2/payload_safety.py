import re


def payload_safety(decrypted_text):
    if re.search(r"unsafe", decrypted_text, re.IGNORECASE):
        return "Unsafe content detected"
    return "Safe content"
