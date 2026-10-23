from __future__ import annotations

from typing import Dict, Optional

from moderate_text import moderate_text
from safety_models import ModerationResult


DEFAULT_THRESHOLDS = {
    "Hate": 2.0,
    "SelfHarm": 1.0,
    "Sexual": 3.0,
    "Violence": 2.0,
}


def safety_threshold(
    text: str, thresholds: Optional[Dict[str, float]] = None, language: str = "en"
) -> ModerationResult:
    result = moderate_text(text=text, language=language)
    effective = dict(DEFAULT_THRESHOLDS)
    effective.update(thresholds or {})
    flagged = any(
        score.severity >= effective.get(score.category, 4.0) for score in result.scores
    )
    result.flagged = flagged
    result.action = "block" if flagged else "allow"
    result.reasons = [
        score.category
        for score in result.scores
        if score.severity >= effective.get(score.category, 4.0)
    ]
    return result
