from __future__ import annotations

import os
import re

from security_models import SecretAnalysisRequest, SecretAnalysisResponse


_SENSITIVE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in [r"password", r"api[_-]?key", r"secret", r"token"]]


def check_secret_label_safety(label: str, notes: str) -> SecretAnalysisResponse:
    request = SecretAnalysisRequest(label=label, notes=notes)
    unsafe = any(pattern.search(request.label) or pattern.search(request.notes) for pattern in _SENSITIVE_PATTERNS)
    risk = "high" if unsafe else "low"
    summary = "Unsafe label or notes detected." if unsafe else "Label and notes appear safe."
    return SecretAnalysisResponse(risk_level=risk, summary=summary, provider=request.provider, metadata={"label": request.label})


if __name__ == "__main__":
    print(check_secret_label_safety(os.environ.get("SECRET_LABEL", "rotation"), os.environ.get("SECRET_NOTES", "")).summary)
