from __future__ import annotations

import os
from typing import Any, Mapping, Optional

import requests

from identity_client import build_identity_headers, identity_endpoint, load_identity_config
from identity_models import ProfileModerationRequest, normalize_locale


OPENAI_API_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _env(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _moderation_client_headers() -> dict[str, str]:
    api_key = _env("OPENAI_API_KEY", required=True)
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _extract_label(result: Mapping[str, Any]) -> str:
    flagged = bool(result.get("flagged"))
    if flagged:
        return "rejected"
    return "approved"


def moderate_profile_text(payload: Mapping[str, Any] | ProfileModerationRequest) -> dict[str, Any]:
    request = payload if isinstance(payload, ProfileModerationRequest) else ProfileModerationRequest.from_mapping(payload)
    cfg = load_identity_config()
    locale = normalize_locale(request.locale)
    response = requests.post(
        f"{OPENAI_API_BASE_URL}/moderations",
        headers=_moderation_client_headers(),
        json={"model": OPENAI_MODERATION_MODEL, "input": request.profile_text},
        timeout=30,
    )
    response.raise_for_status()
    moderation = response.json()
    result = (moderation.get("results") or [{}])[0]
    label = _extract_label(result)
    reason = "profile text passed moderation" if label == "approved" else "profile text was flagged by OpenAI moderation"
    support_note = {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "label": label,
        "locale": locale,
        "reason": reason,
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "identity_base_url": cfg.api_base_url,
    }
    return {
        "ok": True,
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "label": label,
        "approved": label == "approved",
        "result": result,
        "support_note": support_note,
        "identity_headers": build_identity_headers(cfg),
        "identity_endpoint": identity_endpoint("profile/moderation", cfg),
    }
