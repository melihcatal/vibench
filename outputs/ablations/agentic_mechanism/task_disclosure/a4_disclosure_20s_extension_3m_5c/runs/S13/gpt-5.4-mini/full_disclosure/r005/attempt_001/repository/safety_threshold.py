import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Optional

import requests


AZURE_AI_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_AI_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
AZURE_AI_CONTENT_SAFETY_API_KEY = os.getenv("AZURE_AI_CONTENT_SAFETY_API_KEY", "")
AZURE_AI_CONTENT_SAFETY_API_VERSION = os.getenv("AZURE_AI_CONTENT_SAFETY_API_VERSION", "2024-09-01")


DEFAULT_THRESHOLDS: Dict[str, int] = {
    "hate": 2,
    "self_harm": 2,
    "sexual": 2,
    "violence": 2,
}


@dataclass(frozen=True)
class ThresholdDecision:
    allow: bool
    triggered_categories: Dict[str, int]
    severities: Dict[str, int]


def _severity_value(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        mapping = {"safe": 0, "low": 1, "medium": 2, "high": 3, "very_high": 4}
        if normalized in mapping:
            return mapping[normalized]
        try:
            return int(float(normalized))
        except ValueError:
            return 0
    return 0


def _extract_severities(result: Mapping[str, Any]) -> Dict[str, int]:
    severities: Dict[str, int] = {}
    for category, value in result.items():
        if isinstance(value, Mapping):
            for key in ("severity", "level", "score"):
                if key in value:
                    severities[category] = _severity_value(value[key])
                    break
        else:
            severities[category] = _severity_value(value)
    return severities


def evaluate_thresholds(
    moderation_result: Mapping[str, Any],
    thresholds: Optional[Mapping[str, int]] = None,
) -> ThresholdDecision:
    threshold_map = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        threshold_map.update({k: int(v) for k, v in thresholds.items()})
    severities = _extract_severities(moderation_result)
    triggered = {category: severity for category, severity in severities.items() if severity >= threshold_map.get(category, 999)}
    return ThresholdDecision(allow=not triggered, triggered_categories=triggered, severities=severities)


def _azure_moderate_text(text: str) -> Mapping[str, Any]:
    if not AZURE_AI_CONTENT_SAFETY_ENDPOINT or not AZURE_AI_CONTENT_SAFETY_API_KEY:
        raise RuntimeError("AZURE_AI_CONTENT_SAFETY_ENDPOINT and AZURE_AI_CONTENT_SAFETY_API_KEY are required")
    url = f"{AZURE_AI_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={AZURE_AI_CONTENT_SAFETY_API_VERSION}"
    response = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": AZURE_AI_CONTENT_SAFETY_API_KEY,
            "Content-Type": "application/json",
        },
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def apply_thresholds(
    text: str,
    thresholds: Optional[Mapping[str, int]] = None,
    moderation_result: Optional[Mapping[str, Any]] = None,
) -> ThresholdDecision:
    result = moderation_result if moderation_result is not None else _azure_moderate_text(text)
    return evaluate_thresholds(result, thresholds=thresholds)
