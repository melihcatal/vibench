from __future__ import annotations

from typing import Any, Dict, Optional

from safety_client import (
    extract_perspective_scores,
    get_default_thresholds,
    perspective_analyze,
)
from safety_models import ModerationDecision, build_decision


def moderate_text(
    text: str,
    *,
    thresholds: Optional[Dict[str, float]] = None,
    language: Optional[str] = None,
) -> ModerationDecision:
    response = perspective_analyze(text, language=language)
    categories = extract_perspective_scores(response)
    return build_decision(
        text=text,
        provider="Perspective API",
        model="commentanalyzer.googleapis.com/v1alpha1",
        categories=categories,
        threshold_map=thresholds or get_default_thresholds(),
        raw_response=response,
    )


def moderate_text_dict(
    text: str,
    *,
    thresholds: Optional[Dict[str, float]] = None,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    decision = moderate_text(text, thresholds=thresholds, language=language)
    return {
        "text": decision.text,
        "flagged": decision.flagged,
        "action": decision.action,
        "provider": decision.provider,
        "model": decision.model,
        "categories": decision.categories,
        "reasons": decision.reasons,
    }
