from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional

import requests

from identity_client import IdentityConfig, build_identity_headers, identity_endpoint, load_identity_config
from identity_models import OnboardingSummaryRequest, normalize_locale


@dataclass(frozen=True)
class OnboardingSummaryResult:
    ok: bool
    user_id: str
    provider: str
    account_status: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    profile_moderation_status: Optional[str] = None
    locale: Optional[str] = None
    support_notes_count: Optional[int] = None
    last_event_at: Optional[str] = None
    summary: Optional[str] = None
    request_id: Optional[str] = None
    raw: Optional[dict[str, Any]] = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "user_id": self.user_id,
            "provider": self.provider,
            "account_status": self.account_status,
            "email": self.email,
            "email_verified": self.email_verified,
            "profile_moderation_status": self.profile_moderation_status,
            "locale": self.locale,
            "support_notes_count": self.support_notes_count,
            "last_event_at": self.last_event_at,
            "summary": self.summary,
            "request_id": self.request_id,
            "raw": self.raw,
        }


def _provider() -> str:
    return "clerk"


def _normalize_summary_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ok": bool(data.get("ok", True)),
        "user_id": str(data.get("user_id", data.get("userId", ""))).strip() or None,
        "provider": str(data.get("provider", _provider())).strip() or _provider(),
        "account_status": str(data.get("account_status", data.get("accountStatus", ""))).strip() or None,
        "email": str(data.get("email", "")).strip() or None,
        "email_verified": bool(data.get("email_verified", data.get("emailVerified", False))),
        "profile_moderation_status": str(data.get("profile_moderation_status", data.get("profileModerationStatus", ""))).strip() or None,
        "locale": normalize_locale(data.get("locale")) if data.get("locale") is not None else None,
        "support_notes_count": int(data["support_notes_count"] if data.get("support_notes_count") is not None else data["supportNotesCount"]) if data.get("support_notes_count") is not None or data.get("supportNotesCount") is not None else None,
        "last_event_at": str(data.get("last_event_at", data.get("lastEventAt", ""))).strip() or None,
        "summary": str(data.get("summary", "")).strip() or None,
        "request_id": str(data.get("request_id", data.get("requestId", ""))).strip() or None,
        "raw": dict(data),
    }


def _summary_text(payload: Mapping[str, Any]) -> str:
    parts = []
    user_id = payload.get("user_id")
    if user_id:
        parts.append(f"user {user_id}")
    account_status = payload.get("account_status")
    if account_status:
        parts.append(f"status {account_status}")
    if payload.get("email"):
        verified = "verified" if payload.get("email_verified") else "unverified"
        parts.append(f"email {payload.get('email')} ({verified})")
    moderation = payload.get("profile_moderation_status")
    if moderation:
        parts.append(f"profile {moderation}")
    notes = payload.get("support_notes_count")
    if notes is not None:
        parts.append(f"{notes} support notes")
    if payload.get("locale"):
        parts.append(f"locale {payload.get('locale')}")
    if payload.get("last_event_at"):
        parts.append(f"last event {payload.get('last_event_at')}")
    return "; ".join(parts) if parts else "onboarding state available"


def summarize_onboarding_state(data: Mapping[str, Any], config: Optional[IdentityConfig] = None) -> OnboardingSummaryResult:
    request = OnboardingSummaryRequest.from_mapping(data)
    cfg = config or load_identity_config()
    payload = _normalize_summary_payload(data)
    payload["user_id"] = request.user_id
    payload["locale"] = request.locale
    payload["provider"] = _provider()
    payload["summary"] = _summary_text(payload)
    return OnboardingSummaryResult(**payload)


def fetch_onboarding_summary(data: Mapping[str, Any], config: Optional[IdentityConfig] = None, timeout: float = 20.0) -> OnboardingSummaryResult:
    request = OnboardingSummaryRequest.from_mapping(data)
    cfg = config or load_identity_config()
    url = identity_endpoint(f"v1/users/{request.user_id}/onboarding-summary", cfg)
    headers = build_identity_headers(cfg)
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    normalized = _normalize_summary_payload(payload if isinstance(payload, Mapping) else {})
    normalized["user_id"] = request.user_id
    normalized["provider"] = _provider()
    normalized["locale"] = request.locale or normalized.get("locale")
    normalized["summary"] = _summary_text(normalized)
    return OnboardingSummaryResult(**normalized)


def onboarding_summary(data: Mapping[str, Any], config: Optional[IdentityConfig] = None, timeout: float = 20.0) -> dict[str, Any]:
    if os.getenv("IDENTITY_FETCH_ONBOARDING_SUMMARY", "").strip().lower() in {"1", "true", "yes"}:
        return fetch_onboarding_summary(data, config=config, timeout=timeout).as_dict()
    return summarize_onboarding_state(data, config=config).as_dict()
