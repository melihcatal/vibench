from __future__ import annotations

import re

from security_models import SafetyCheck

UNSAFE_PATTERNS = [r"\bpassword\b", r"\bsecret\b", r"\bssn\b", r"\bprivate key\b"]


def payload_safety(text: str) -> dict:
    lowered = text.lower()
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, lowered):
            return SafetyCheck(payload=text, unsafe=True, reason=f"matched:{pattern}").__dict__
    return SafetyCheck(payload=text, unsafe=False, reason="no unsafe indicators").__dict__
