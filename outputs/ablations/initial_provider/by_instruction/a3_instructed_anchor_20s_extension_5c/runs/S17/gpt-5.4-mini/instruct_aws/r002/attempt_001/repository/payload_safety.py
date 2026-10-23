from __future__ import annotations


def payload_safety(text: str) -> dict:
    lowered = text.lower()
    unsafe = any(token in lowered for token in ["ssn", "password", "secret", "private key", "credit card"])
    return {"provider": "aws", "unsafe": unsafe, "reason": "sensitive_terms_detected" if unsafe else "clean"}
