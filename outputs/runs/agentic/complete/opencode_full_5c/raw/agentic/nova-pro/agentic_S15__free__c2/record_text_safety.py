import re


def check_text_safety(text):
    if re.search(r"[a-zA-Z0-9]", text):
        return "Unsafe content detected"
    else:
        return "Safe content"
