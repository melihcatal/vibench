from __future__ import annotations

from moderate_text import moderate_text


DEFAULT_THRESHOLDS = {
    "hate": 3,
    "sexual": 5,
    "self_harm": 2,
    "violence": 4,
}


def safety_threshold(
    text: str, thresholds: dict[str, int] | None = None, language: str | None = None
) -> dict[str, object]:
    result = moderate_text(text=text, language=language)
    applied = thresholds or DEFAULT_THRESHOLDS
    severity_map = result.severity_map()
    allow = all(
        severity_map.get(category, 0) < limit for category, limit in applied.items()
    )
    return {
        "allow": allow,
        "thresholds": applied,
        "scores": severity_map,
        "provider": result.provider,
    }
