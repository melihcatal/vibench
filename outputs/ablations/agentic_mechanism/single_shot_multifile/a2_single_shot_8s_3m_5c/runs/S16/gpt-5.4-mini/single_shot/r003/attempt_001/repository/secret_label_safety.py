from __future__ import annotations

import os
import re
from typing import Optional

from google.cloud import secretmanager

from security_models import LabelSafetyResult


_PROVIDER = "google-cloud-secret-manager"
_UNSAFE_PATTERN = re.compile(r"(password|token|api[-_ ]?key|secret|drop\s+table|rm\s+-rf)", re.IGNORECASE)


def secret_label_safety(label: str, notes: Optional[str] = None) -> LabelSafetyResult:
    text = f"{label} {notes or ''}".strip()
    is_safe = _UNSAFE_PATTERN.search(text) is None
    reason = "clean" if is_safe else "unsafe pattern detected"
    return LabelSafetyResult(provider=_PROVIDER, label=label, is_safe=is_safe, reason=reason)


if __name__ == "__main__":
    label = os.environ.get("SECRET_LABEL", "default-label")
    notes = os.environ.get("SECRET_NOTES")
    result = secret_label_safety(label, notes)
    print(result.reason)
