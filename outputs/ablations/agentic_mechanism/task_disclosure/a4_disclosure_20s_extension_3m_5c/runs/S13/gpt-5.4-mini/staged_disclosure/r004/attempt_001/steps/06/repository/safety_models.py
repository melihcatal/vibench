import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
DEFAULT_MODERATION_MODEL = "omni-moderation-latest"


@dataclass(frozen=True)
class SafetyRequest:
    text: str
    model: str = DEFAULT_MODERATION_MODEL


@dataclass(frozen=True)
class SafetyResponse:
    unsafe: bool
    risk_score: float
    categories: List[str] = field(default_factory=list)
    explanation: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)


def load_safety_request(text: str, model: Optional[str] = None) -> SafetyRequest:
    return SafetyRequest(text=text, model=model or os.getenv("OPENAI_MODERATION_MODEL", DEFAULT_MODERATION_MODEL))


def normalize_safety_response(payload: Mapping[str, Any]) -> SafetyResponse:
    results = payload.get("results", []) if isinstance(payload, Mapping) else []
    if not results:
        return SafetyResponse(unsafe=False, risk_score=0.0, categories=[], explanation="", raw=dict(payload) if isinstance(payload, Mapping) else {})

    result = results[0] if isinstance(results[0], Mapping) else {}
    category_scores = result.get("category_scores", {}) if isinstance(result, Mapping) else {}
    categories = [name for name, score in category_scores.items() if float(score or 0.0) > 0.0]
    unsafe = bool(result.get("flagged", False)) if isinstance(result, Mapping) else False
    risk_score = max((float(score or 0.0) for score in category_scores.values()), default=0.0)
    return SafetyResponse(
        unsafe=unsafe,
        risk_score=risk_score,
        categories=categories,
        explanation=str(result.get("category_applied_input_types", "")) if isinstance(result, Mapping) else "",
        raw=dict(payload),
    )


def moderate_text(text: str, api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 30) -> SafetyResponse:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    request = load_safety_request(text=text, model=model)
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": request.model, "input": request.text},
        timeout=timeout,
    )
    response.raise_for_status()
    return normalize_safety_response(response.json())
