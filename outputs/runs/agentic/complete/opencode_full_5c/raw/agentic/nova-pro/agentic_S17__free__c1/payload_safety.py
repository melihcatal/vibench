import re


def check_decrypted_text(text):
    if re.search(r"unsafe_content", text):
        return "Unsafe content detected"
    return "Safe content"
