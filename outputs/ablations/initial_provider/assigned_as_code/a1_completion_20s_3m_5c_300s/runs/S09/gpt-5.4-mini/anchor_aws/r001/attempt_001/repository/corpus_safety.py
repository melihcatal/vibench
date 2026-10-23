import re


def corpus_safety(payload, config=None):
    text = payload["text"]
    unsafe = bool(re.search(r"\b(password|secret|ssn|credit card)\b", text, re.I))
    return {"safe": not unsafe, "reason": None if not unsafe else "sensitive_content_detected"}
