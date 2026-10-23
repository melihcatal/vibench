from __future__ import annotations

import re
from typing import Dict, List

from safety_client import PerspectiveSafetyClient, extract_attribute_scores
from safety_models import RedactionSpan, merge_text_spans, normalize_scores


UNSAFE_PATTERNS: Dict[str, List[str]] = {
    "threat": [r"\bkill\b", r"\bhurt\b", r"\battack\b"],
    "insult": [r"\bidiot\b", r"\bstupid\b", r"\bmoron\b"],
    "profanity": [r"\bdamn\b", r"\bhell\b"],
}


def redact_unsafe(text: str, language: str = "en", threshold: float = 0.75) -> dict:
    client = PerspectiveSafetyClient()
    raw = client.analyze_text(text=text, language=language)
    normalized = normalize_scores(extract_attribute_scores(raw))
    spans: List[RedactionSpan] = []
    for category, score in normalized.items():
        if score.score < threshold or category not in UNSAFE_PATTERNS:
            continue
        for pattern in UNSAFE_PATTERNS[category]:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                spans.append(RedactionSpan(start=match.start(), end=match.end(), category=category))
    redacted_text = merge_text_spans(text, spans)
    return {
        "provider": "Perspective API",
        "model": client.model,
        "flagged": bool(spans),
        "redacted_text": redacted_text,
        "spans": [span.__dict__ for span in spans],
        "scores": {name: item.score for name, item in normalized.items()},
    }
