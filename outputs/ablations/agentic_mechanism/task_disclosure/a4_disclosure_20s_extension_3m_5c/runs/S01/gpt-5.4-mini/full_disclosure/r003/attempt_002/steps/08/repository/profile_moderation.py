from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from typing import Any, Dict, Mapping, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_MODERATION_ENDPOINT = "https://api.openai.com/v1/moderations"


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _normalize_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def _normalize_bool(value: Any) -> Optional[bool]:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "1", "yes", "y", "on"}:
            return True
        if v in {"false", "0", "no", "n", "off"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None


@dataclass(frozen=True)
class ProfileModerationRequest:
    text: str
    locale: Optional[str] = None
    user_id: Optional[str] = None

    def normalized(self) -> "ProfileModerationRequest":
        return ProfileModerationRequest(
            text=_normalize_string(self.text) or self.text,
            locale=_normalize_string(self.locale),
            user_id=_normalize_string(self.user_id),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProfileModerationResult:
    approved: bool
    flagged: bool
    category_scores: Dict[str, float]
    categories: Dict[str, bool]
    raw_response: Dict[str, Any]
    model: str
    reason: Optional[str] = None

    @classmethod
    def from_openai_response(cls, payload: Mapping[str, Any]) -> "ProfileModerationResult":
        results = payload.get("results") or []
        first = results[0] if results else {}
        categories = first.get("categories") or {}
        scores = first.get("category_scores") or {}
        flagged = bool(first.get("flagged", False))
        approved = not flagged
        reason = None
        if flagged:
            reason = next((name for name, value in categories.items() if value), None)
        return cls(
            approved=approved,
            flagged=flagged,
            category_scores={str(k): float(v) for k, v in scores.items() if v is not None},
            categories={str(k): bool(v) for k, v in categories.items()},
            raw_response=dict(payload),
            model=str(payload.get("model") or OPENAI_MODERATION_MODEL),
            reason=reason,
        )


def moderate_profile_text(text: str, locale: Optional[str] = None, user_id: Optional[str] = None, api_key: Optional[str] = None, model: str = OPENAI_MODERATION_MODEL, timeout: int = 30) -> ProfileModerationResult:
    request = ProfileModerationRequest(text=text, locale=locale, user_id=user_id).normalized()
    key = api_key or _env("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    payload = {"model": model, "input": request.text}
    if request.locale:
        payload["locale"] = request.locale
    body = json.dumps(payload).encode("utf-8")
    req = Request(OPENAI_MODERATION_ENDPOINT, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc)
        raise RuntimeError(f"OpenAI moderation request failed: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"OpenAI moderation request failed: {exc}") from exc
    return ProfileModerationResult.from_openai_response(data)
