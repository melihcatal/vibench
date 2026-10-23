from __future__ import annotations

import re
from typing import Any, Dict, List

from security_models import normalize_text

UNSAFE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in [r"\bpassword\b", r"\bssn\b", r"credit card", r"\bsecret\b", r"\bprivate key\b"]]


def payload_safety(payload: Any) -> Dict[str, Any]:
    text = normalize_text(payload)
    findings: List[str] = []
    for pattern in UNSAFE_PATTERNS:
        if pattern.search(text):
            findings.append(pattern.pattern)
    return {"safe": not findings, "findings": findings, "length": len(text)}
