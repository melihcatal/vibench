import re


def message_safety(payload_text):
    unsafe = bool(re.search(r"\b(password|secret|ssn|credit card)\b", payload_text.lower()))
    return {"provider": "google.pubsub_v1", "safe": not unsafe, "reason": None if not unsafe else "sensitive_keyword_detected"}
