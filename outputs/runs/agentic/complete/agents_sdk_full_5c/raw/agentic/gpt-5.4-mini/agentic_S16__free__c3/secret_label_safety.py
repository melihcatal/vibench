from __future__ import annotations

import re

from security_models import SafetyCheckResult

# AWS Secrets Manager integration
UNSAFE_PATTERNS = [r"(?i)password", r"(?i)token", r"(?i)secret", r"(?i)drop\s+table", r"(?i)rm\s+-rf"]


def secret_label_safety(label: str, note: str) -> SafetyCheckResult:
    reasons = []
    text = f"{label} {note}"
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, text):
            reasons.append(pattern)
    return SafetyCheckResult(label=label, note=note, unsafe=bool(reasons), reasons=reasons)
