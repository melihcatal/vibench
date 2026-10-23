import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import requests

from identity_client import build_identity_headers, build_identity_url, get_identity_timeout_seconds
from identity_models import IdentityModelError, normalize_metadata, normalize_trimmed_text


OPENAI_API_HOST = "https://api.openai.com"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


@dataclass(frozen=True)
class ProfileModerationRequest:
    profile_text: str
    locale: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "ProfileModerationRequest":
        text = normalize_trimmed_text(self.profile_text, field_name="profile_text")
        if text is None:
            raise IdentityModelError("profile_text cannot be empty")
        locale = normalize_trimmed_text(self.locale, field_name="locale", allow_empty=False) or "en"
        return ProfileModerationRequest(
            profile_text=text,
            locale=locale,
            metadata=normalize_metadata(self.metadata),
        )


@dataclass(frozen=True)
class ProfileModerationResult:
    approved: bool
    flagged: bool
    categories: Dict[str, Any]
    category_scores: Dict[str, Any]
    provider: str
    raw: Dict[str, Any]


def _openai_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise IdentityModelError("OPENAI_API_KEY is required for profile moderation")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    return headers


def moderate_profile_text(request: ProfileModerationRequest) -> ProfileModerationResult:
    normalized = request.normalized()
    payload = {"model": OPENAI_MODERATION_MODEL, "input": normalized.profile_text}
    response = requests.post(
        f"{OPENAI_API_HOST}/v1/moderations",
        headers=_openai_headers(),
        json=payload,
        timeout=get_identity_timeout_seconds(),
    )
    response.raise_for_status()
    data = response.json()
    result = data.get("results", [{}])[0]
    categories = result.get("categories", {}) or {}
    scores = result.get("category_scores", {}) or {}
    flagged = bool(result.get("flagged", False))
    approved = not flagged
    return ProfileModerationResult(
        approved=approved,
        flagged=flagged,
        categories=categories,
        category_scores=scores,
        provider="openai",
        raw=data,
    )


def moderate_profile_with_identity_context(profile_text: str, locale: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> ProfileModerationResult:
    _ = build_identity_url("/profile/moderation")
    _ = build_identity_headers()
    request = ProfileModerationRequest(profile_text=profile_text, locale=locale or "en", metadata=metadata or {})
    return moderate_profile_text(request)
