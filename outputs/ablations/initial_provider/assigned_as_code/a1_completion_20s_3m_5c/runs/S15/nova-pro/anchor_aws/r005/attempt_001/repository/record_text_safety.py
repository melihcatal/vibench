import re


def record_text_safety(document):
    if not document:
        return True
    for key, value in document.items():
        if isinstance(value, str):
            if re.search(r"[^a-zA-Z0-9\s]", value):
                return False
    return True