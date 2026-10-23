import os
from typing import Any, Dict, Iterable, Optional
import requests

from safety_models import ModerationDecision, normalize_text, normalize_thresholds, to_message_list

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_api_key() -> str:
    key = os.getenv("PERSPECTIVE_API_KEY", "").strip()
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    return key


def _headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def _params() -> Dict[str, str]:
    return {"key": get_api_key()}


def perspective_analyze(text: str, attributes: Optional[Iterable[str]] = None) -> Dict[str, Any]:
    attrs = list(attributes) if attributes is not None else ["TOXICITY", "INSULT", "THREAT", "PROFANITY", "SEXUALLY_EXPLICIT", "IDENTITY_ATTACK"]
    payload = {"comment": {"text": normalize_text(text)}, "languages": ["en"], "requestedAttributes": {name: {} for name in attrs}}
    response = requests.post(PERSPECTIVE_API_URL, params=_params(), headers=_headers(), json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def parse_perspective_scores(data: Dict[str, Any]) -> Dict[str, float]:
    result = {}
    for key, value in (data.get("attributeScores") or {}).items():
        summary = (value or {}).get("summaryScore") or {}
        result[key.lower()] = float(summary.get("value", 0.0))
    return result


def moderate_text(text: str, thresholds: Optional[Dict[str, float]] = None) -> ModerationDecision:
    data = perspective_analyze(text)
    scores = parse_perspective_scores(data)
    th = normalize_thresholds(thresholds)
    allowed = all(scores.get(cat, 0.0) < limit for cat, limit in th.items())
    return ModerationDecision(allowed=allowed, scores=scores, raw=data)


def moderate_messages(messages: Iterable[str], thresholds: Optional[Dict[str, float]] = None):
    return [moderate_text(message, thresholds=thresholds) for message in to_message_list(messages)]
