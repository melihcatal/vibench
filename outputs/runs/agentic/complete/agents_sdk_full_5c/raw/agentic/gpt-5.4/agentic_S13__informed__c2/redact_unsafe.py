from __future__ import annotations

import re
from typing import Dict, List, Optional

from safety_client import PerspectiveSafetyClient
from safety_models import SafetyRequest


DEFAULT_REDACTION_PATTERNS: Dict[str, List[str]] = {
    "threat": [r"\bkill\b", r"\bhurt\b", r"\battack\b", r"\bshoot\b"],
    "profanity": [r"\bfuck\b", r"\bshit\b", r"\bbitch\b"],
    "identity_attack": [r"\bidiot\b", r"\bmoron\b"],
}


def redact_unsafe(
    text: str,
    language: Optional[str] = None,
    threshold: float = 0.7,
    client: Optional[PerspectiveSafetyClient] = None,
) -> Dict[str, object]:
    moderation_client = client or PerspectiveSafetyClient(
        requested_attributes=["TOXICITY", "THREAT", "PROFANITY", "IDENTITY_ATTACK"]
    )
    raw = moderation_client.analyze(SafetyRequest(text=text, language=language))
    attributes = raw.get("attributeScores", {})
    redacted = text
    triggered_categories: List[str] = []

    for raw_name, payload in attributes.items():
        score = float(payload.get("summaryScore", {}).get("value", 0.0))
        category = raw_name.lower()
        if score < threshold:
            continue
        triggered_categories.append(category)
        for pattern in DEFAULT_REDACTION_PATTERNS.get(category, []):
            redacted = re.sub(pattern, "[REDACTED]", redacted, flags=re.IGNORECASE)

    return {
        "provider": "Perspective API",
        "flagged": bool(triggered_categories),
        "categories": triggered_categories,
        "redacted_text": redacted,
        "raw_response": raw,
    }
