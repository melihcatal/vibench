from __future__ import annotations

from typing import Iterable, List

from safety_client import PerspectiveSafetyClient, extract_attribute_scores
from safety_models import BatchModerationDecision, ModerationResult, normalize_scores


DEFAULT_FLAG_THRESHOLD = 0.7


def moderate_batch(messages: Iterable[str], language: str = "en") -> List[dict]:
    client = PerspectiveSafetyClient()
    decisions: List[dict] = []
    for index, text in enumerate(messages):
        raw = client.analyze_text(text=text, language=language)
        scores = extract_attribute_scores(raw)
        normalized = normalize_scores(scores)
        result = ModerationResult(
            text=text,
            provider="Perspective API",
            model=client.model,
            flagged=any(item.score >= DEFAULT_FLAG_THRESHOLD for item in normalized.values()),
            categories=normalized,
            raw_response=raw,
        )
        decisions.append(
            {
                "index": BatchModerationDecision(index=index, text=text, result=result).index,
                "text": text,
                "decision": result.as_dict(),
            }
        )
    return decisions
