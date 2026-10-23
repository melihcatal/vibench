from __future__ import annotations

import re
from typing import Any, Dict

from safety_client import analyze_text, highest_category
from safety_models import SafetyRequest, to_serializable_result


def redact_unsafe(text: str, language: str = "en") -> Dict[str, Any]:
    result = analyze_text(SafetyRequest(text=text, language=language))
    strongest = highest_category(result.categories)
    if result.flagged and strongest and strongest.score >= 0.7:
        redacted_text = re.sub(r"\S+", "[REDACTED]", text)
        result.redacted_text = redacted_text
        result.unsafe_spans = [
            {"start": 0, "end": len(text), "category": strongest.name}
        ]
    else:
        result.redacted_text = text
    return to_serializable_result(result)
