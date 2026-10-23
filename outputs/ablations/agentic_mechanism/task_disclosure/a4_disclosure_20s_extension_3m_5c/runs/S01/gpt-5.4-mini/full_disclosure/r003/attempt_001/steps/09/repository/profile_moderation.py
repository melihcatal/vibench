import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
OPENAI_MODERATION_ENDPOINT = os.getenv("OPENAI_MODERATION_ENDPOINT", "https://api.openai.com/v1/moderations")


class ProfileModerationError(Exception):
    pass


@dataclass(frozen=True)
class ProfileModerationRequest:
    text: str
    user_id: Optional[str] = None
    locale: Optional[str] = None


@dataclass(frozen=True)
class ProfileModerationResult:
    approved: bool
    flagged: bool
    model: str
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Dict[str, Any]


def _clean_str(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def _clean_dict(value: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(value) if value else {}


def normalize_profile_moderation_request(payload: Mapping[str, Any]) -> ProfileModerationRequest:
    return ProfileModerationRequest(
        text=_clean_str(payload.get("text")) or "",
        user_id=_clean_str(payload.get("user_id")),
        locale=_clean_str(payload.get("locale")),
    )


def moderate_profile_text(text: str, user_id: Optional[str] = None, locale: Optional[str] = None, api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 30) -> ProfileModerationResult:
    resolved_text = _clean_str(text) or ""
    if not resolved_text:
        raise ProfileModerationError("profile text is required")

    resolved_api_key = _clean_str(api_key) or OPENAI_API_KEY
    if not resolved_api_key:
        raise ProfileModerationError("OPENAI_API_KEY is required")

    request_model = model or OPENAI_MODERATION_MODEL
    response = requests.post(
        OPENAI_MODERATION_ENDPOINT,
        headers={"Authorization": f"Bearer {resolved_api_key}", "Content-Type": "application/json"},
        json={"model": request_model, "input": resolved_text},
        timeout=timeout,
    )

    if response.status_code >= 400:
        raise ProfileModerationError(f"OpenAI moderation request failed: {response.status_code}")

    payload = response.json()
    results = payload.get("results") or []
    if not results:
        raise ProfileModerationError("OpenAI moderation response missing results")

    first = results[0] or {}
    categories = _clean_dict(first.get("categories"))
    category_scores = _clean_dict(first.get("category_scores"))
    flagged = bool(first.get("flagged"))
    approved = not flagged

    return ProfileModerationResult(
        approved=approved,
        flagged=flagged,
        model=_clean_str(payload.get("model")) or request_model,
        categories={str(k): bool(v) for k, v in categories.items()},
        category_scores={str(k): float(v) for k, v in category_scores.items() if v is not None},
        raw=payload,
    )
