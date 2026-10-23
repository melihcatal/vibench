from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

import requests


FIREBASE_LOOKUP_URL = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else default


def _pick(mapping: Mapping[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in mapping and mapping[name] is not None:
            return mapping[name]
    return default


def _str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _normalize_email(value: Any) -> str:
    return _str(value).strip().lower()


def _normalize_locale(value: Any) -> str:
    return _str(value).strip().replace("_", "-").lower()


def _coerce_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "on", "active", "enabled"}:
        return True
    if text in {"false", "0", "no", "n", "off", "inactive", "disabled"}:
        return False
    return default


def _coerce_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class OnboardingSummaryRequest:
    email: str = ""
    user_id: str = ""
    locale: str = ""

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "OnboardingSummaryRequest":
        return cls(
            email=_normalize_email(_pick(data, "email", "username")),
            user_id=_str(_pick(data, "user_id", "uid", "id", "sub")),
            locale=_normalize_locale(_pick(data, "locale")),
        )


@dataclass(frozen=True)
class OnboardingSummary:
    provider: str = "firebase_auth"
    user_id: str = ""
    email: str = ""
    locale: str = ""
    display_name: str = ""
    is_active: bool = False
    email_verified: bool = False
    onboarding_step: str = ""
    profile_complete: bool = False
    moderation_status: str = "unknown"
    created_at: str = ""
    last_sign_in_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "OnboardingSummary":
        return cls(
            provider=_str(_pick(data, "provider", default="firebase_auth")),
            user_id=_str(_pick(data, "user_id", "id", "uid", "sub")),
            email=_normalize_email(_pick(data, "email")),
            locale=_normalize_locale(_pick(data, "locale")),
            display_name=_str(_pick(data, "display_name", "name")),
            is_active=_coerce_bool(_pick(data, "is_active", "active")),
            email_verified=_coerce_bool(_pick(data, "email_verified", "verified_email")),
            onboarding_step=_str(_pick(data, "onboarding_step", "step", "state")),
            profile_complete=_coerce_bool(_pick(data, "profile_complete", "profile_ready")),
            moderation_status=_str(_pick(data, "moderation_status", default="unknown")),
            created_at=_str(_pick(data, "created_at", "createdAt")),
            last_sign_in_at=_str(_pick(data, "last_sign_in_at", "lastSignInAt")),
            metadata=dict(_pick(data, "metadata", default={}) or {}),
        )


def _firebase_api_key() -> str:
    key = _env("FIREBASE_WEB_API_KEY") or _env("GOOGLE_API_KEY") or _env("IDENTITY_API_KEY")
    if not key:
        raise ValueError("Missing Firebase API key; set FIREBASE_WEB_API_KEY, GOOGLE_API_KEY, or IDENTITY_API_KEY")
    return key


def _lookup_user(email: str = "", user_id: str = "") -> Dict[str, Any]:
    payload: Dict[str, Any] = {"key": _firebase_api_key()}
    if user_id:
        payload["localId"] = [user_id]
    elif email:
        payload["email"] = [email]
    else:
        raise ValueError("Either email or user_id is required")
    response = requests.post(FIREBASE_LOOKUP_URL, params={"key": payload.pop("key")}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def summarize_onboarding_state(data: Mapping[str, Any]) -> OnboardingSummary:
    request = OnboardingSummaryRequest.from_mapping(data)
    source = dict(data)
    if not any((request.email, request.user_id)):
        return OnboardingSummary.from_mapping(source)
    remote = _lookup_user(email=request.email, user_id=request.user_id)
    users = remote.get("users") or []
    profile = users[0] if users else {}
    merged: Dict[str, Any] = dict(source)
    merged.update(profile)
    if request.email and not merged.get("email"):
        merged["email"] = request.email
    if request.user_id and not merged.get("user_id"):
        merged["user_id"] = request.user_id
    if "emailVerified" in profile and "email_verified" not in merged:
        merged["email_verified"] = profile.get("emailVerified")
    if "createdAt" in profile and "created_at" not in merged:
        merged["created_at"] = profile.get("createdAt")
    if "lastLoginAt" in profile and "last_sign_in_at" not in merged:
        merged["last_sign_in_at"] = profile.get("lastLoginAt")
    if "disabled" in profile and "is_active" not in merged:
        merged["is_active"] = not _coerce_bool(profile.get("disabled"))
    return OnboardingSummary.from_mapping(merged)


def onboarding_summary(data: Mapping[str, Any]) -> Dict[str, Any]:
    summary = summarize_onboarding_state(data)
    return {
        "provider": summary.provider,
        "user_id": summary.user_id,
        "email": summary.email,
        "locale": summary.locale,
        "display_name": summary.display_name,
        "is_active": summary.is_active,
        "email_verified": summary.email_verified,
        "onboarding_step": summary.onboarding_step,
        "profile_complete": summary.profile_complete,
        "moderation_status": summary.moderation_status,
        "created_at": summary.created_at,
        "last_sign_in_at": summary.last_sign_in_at,
        "metadata": summary.metadata,
    }
