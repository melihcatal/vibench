from typing import Dict
import re


def check_payload_safety(payload: str, metadata: Dict[str, str] = None) -> dict:
    if metadata is None:
        metadata = {}

    safety_checks = {
        "contains_pii": False,
        "pii_types": [],
        "contains_malicious_patterns": False,
        "malicious_patterns": [],
        "entropy_score": 0.0,
        "is_base64_encoded": False,
        "metadata": metadata,
    }

    # Check for PII patterns
    pii_patterns = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\+?[0-9]{10,15}",
        "credit_card": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11})\b",
        "ssn": r"\b(?!000|666)[0-8][0-9]{2}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}\b",
    }

    for pii_type, pattern in pii_patterns.items():
        if re.search(pattern, payload):
            safety_checks["contains_pii"] = True
            safety_checks["pii_types"].append(pii_type)

    # Check for malicious patterns
    malicious_patterns = {
        "sql_injection": r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|OR|AND)\b.*\b(FROM|WHERE|SET|VALUES)\b)|(--|#|/\*|\*/|;)",
        "xss": r"(<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>)|(javascript:)|(on\w+\s*=)",
        "command_injection": r"(\b(cat|ls|rm|mkdir|wget|curl|bash|sh|exec|chmod)\b)|(\|\s*\|)|(&&\s*)|(;\s*)",
    }

    for pattern_type, pattern in malicious_patterns.items():
        if re.search(pattern, payload, re.IGNORECASE):
            safety_checks["contains_malicious_patterns"] = True
            safety_checks["malicious_patterns"].append(pattern_type)

    # Check if payload is base64 encoded
    try:
        if re.match(r"^[A-Za-z0-9+/]+={0,2}$", payload):
            decoded = payload.encode("utf-8")
            if base64.b64encode(base64.b64decode(decoded)).decode("utf-8") == payload:
                safety_checks["is_base64_encoded"] = True
    except Exception:
        pass

    # Calculate entropy score
    if len(payload) > 0:
        freq = {}
        for char in payload:
            freq[char] = freq.get(char, 0) + 1
        entropy = 0.0
        for count in freq.values():
            p = count / len(payload)
            entropy -= p * (p * math.log2(p) if p > 0 else 0)
        safety_checks["entropy_score"] = entropy

    return safety_checks


import math
import base64
