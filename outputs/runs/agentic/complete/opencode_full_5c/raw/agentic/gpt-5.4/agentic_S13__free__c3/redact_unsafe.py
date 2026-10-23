from __future__ import annotations

import re
from typing import Dict, List

from safety_client import (
    PERSPECTIVE_API_URL,
    default_session,
    perspective_api_key,
    perspective_requested_attributes,
)
from safety_models import (
    SafetyDecision,
    SafetyRequest,
    SafetySpan,
    normalize_category_scores,
)


UNSAFE_TERMS = {
    "threat": [r"\\bkill\\b", r"\\bmurder\\b", r"\\bshoot\\b"],
    "profanity": [r"\\bfuck\\b", r"\\bshit\\b"],
    "insult": [r"\\bidiot\\b", r"\\bstupid\\b"],
}


def _extract_spans(text: str, scores: Dict[str, float]) -> List[SafetySpan]:
    spans: List[SafetySpan] = []
    for label, patterns in UNSAFE_TERMS.items():
        label_score = scores.get(label, 0.0)
        if label_score < 0.5:
            continue
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                spans.append(
                    SafetySpan(
                        start=match.start(),
                        end=match.end(),
                        label=label,
                        text=match.group(0),
                        score=label_score,
                    )
                )
    return sorted(spans, key=lambda span: (span.start, span.end))


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> SafetyDecision:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": perspective_requested_attributes(),
        "doNotStore": True,
    }
    session = default_session()
    response = session.post(
        PERSPECTIVE_API_URL,
        params={"key": perspective_api_key()},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = normalize_category_scores(
        {
            name.lower(): details.get("summaryScore", {}).get("value", 0.0)
            for name, details in data.get("attributeScores", {}).items()
        }
    )
    spans = _extract_spans(text, scores)
    redacted = text
    for span in reversed(spans):
        redacted = redacted[: span.start] + replacement + redacted[span.end :]
    action = "allow" if not spans else "redact"
    return SafetyDecision(
        allowed=not spans,
        action=action,
        flagged_categories=sorted({span.label for span in spans}),
        scores=scores,
        spans=[SafetySpan(**{**span.__dict__, "text": replacement}) for span in spans],
        provider="google_perspective_api",
        raw={"perspective": data, "redacted_text": redacted},
    )
