from __future__ import annotations

import os
import re
from typing import List

from security_models import TextSafetyResult

LABEL = os.getenv("SECRET_LABEL", "customer-facing")
NOTES = os.getenv("SECRET_NOTES", "rotate quarterly and never print values")
UNSAFE_PATTERNS = [r"password\s*[:=]", r"api[_-]?key\s*[:=]", r"secret\s*[:=]", r"do not log", r"plaintext"]


def check_label_and_notes(label: str = LABEL, notes: str = NOTES) -> TextSafetyResult:
    text = f"{label}\n{notes}".lower()
    reasons: List[str] = []
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            reasons.append(pattern)
    unsafe = bool(reasons)
    return TextSafetyResult(label=label, unsafe=unsafe, reasons=tuple(reasons))
