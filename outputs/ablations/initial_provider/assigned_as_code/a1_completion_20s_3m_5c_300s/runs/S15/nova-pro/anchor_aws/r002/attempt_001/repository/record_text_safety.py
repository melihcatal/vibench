import re


def record_text_safety(document):
    if not document:
        return True
    for field in document:
        if isinstance(document[field], str):
            if re.search(r"[^a-zA-Z0-9\s]", document[field]):
                return False
    return True