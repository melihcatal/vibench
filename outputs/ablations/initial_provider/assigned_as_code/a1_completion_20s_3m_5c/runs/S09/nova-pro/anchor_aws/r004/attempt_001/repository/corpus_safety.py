import re


def corpus_safety(text):
    if re.search(r"[^a-zA-Z0-9\s]", text):
        return {"safe": False, "reason": "Text contains invalid characters"}
    return {"safe": True}