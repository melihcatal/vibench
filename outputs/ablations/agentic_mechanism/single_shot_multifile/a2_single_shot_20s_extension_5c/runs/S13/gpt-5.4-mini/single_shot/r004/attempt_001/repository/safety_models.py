import json
from typing import Any, Dict, List


def _loads_maybe(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        return json.loads(value)
    raise TypeError("Expected dict or JSON string")


def normalize_moderation_result(payload: Any) -> Dict[str, Any]:
    data = _loads_maybe(payload)
    data.setdefault("allow", True)
    data.setdefault("categories", {})
    data.setdefault("rationale", "")
    return data


def normalize_batch_input(messages: List[str]) -> List[str]:
    return [str(message) for message in messages]


def normalize_redaction_result(payload: Any) -> Dict[str, Any]:
    data = _loads_maybe(payload)
    data.setdefault("redacted_text", "")
    data.setdefault("spans", [])
    return data


def normalize_threshold_result(payload: Any, thresholds: Dict[str, float] | None = None) -> Dict[str, Any]:
    data = _loads_maybe(payload)
    data.setdefault("decision", "allow")
    data.setdefault("category_scores", {})
    if thresholds is not None:
        data["thresholds"] = thresholds
    return data
