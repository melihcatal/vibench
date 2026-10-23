from __future__ import annotations

import re
from typing import Dict, List, Optional

from safety_client import (
    extract_perspective_scores,
    get_default_thresholds,
    perspective_analyze,
)
from safety_models import ModerationDecision, build_decision


ATTRIBUTE_PATTERNS = {
    "threat": [r"\bkill\b", r"\bhurt\b", r"\battack\b"],
    "profanity": [r"\bfuck\b", r"\bshit\b", r"\bbitch\b"],
    "insult": [r"\bidiot\b", r"\bstupid\b", r"\bmoron\b"],
    "identity_attack": [r"\b(?:race|religion|ethnicity)\b"],
}


def _find_unsafe_spans(
    text: str, categories: Dict[str, float], thresholds: Dict[str, float]
) -> List[Dict[str, object]]:
    spans: List[Dict[str, object]] = []
    for category, score in categories.items():
        if score < float(thresholds.get(category, 0.5)):
            continue
        for pattern in ATTRIBUTE_PATTERNS.get(category, []):
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                spans.append(
                    {
                        "category": category,
                        "score": score,
                        "start": match.start(),
                        "end": match.end(),
                        "text": match.group(0),
                    }
                )
    spans.sort(key=lambda item: (int(item["start"]), int(item["end"])))
    return spans


def _apply_redactions(text: str, spans: List[Dict[str, object]]) -> str:
    if not spans:
        return text
    pieces = []
    cursor = 0
    for span in spans:
        start = int(span["start"])
        end = int(span["end"])
        if start < cursor:
            continue
        pieces.append(text[cursor:start])
        pieces.append("[REDACTED]")
        cursor = end
    pieces.append(text[cursor:])
    return "".join(pieces)


def redact_unsafe(
    text: str,
    *,
    thresholds: Optional[Dict[str, float]] = None,
    language: Optional[str] = None,
) -> ModerationDecision:
    response = perspective_analyze(text, language=language)
    categories = extract_perspective_scores(response)
    active_thresholds = thresholds or get_default_thresholds()
    spans = _find_unsafe_spans(text, categories, active_thresholds)
    redacted_text = _apply_redactions(text, spans)
    return build_decision(
        text=text,
        provider="Perspective API",
        model="commentanalyzer.googleapis.com/v1alpha1",
        categories=categories,
        threshold_map=active_thresholds,
        unsafe_spans=spans,
        redacted_text=redacted_text,
        raw_response=response,
    )
