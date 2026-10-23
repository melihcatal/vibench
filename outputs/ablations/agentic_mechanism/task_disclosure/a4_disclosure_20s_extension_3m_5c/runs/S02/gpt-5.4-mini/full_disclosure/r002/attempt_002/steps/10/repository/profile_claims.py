from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional

import requests

GOOGLE_OIDC_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


@dataclass(frozen=True)
class NormalizedProfileClaims:
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    display_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture_url: Optional[str]
    locale: Optional[str]
    raw_provider: str


def _compact(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _boolish(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "on"}:
        return True
    if text in {"false", "0", "no", "n", "off"}:
        return False
    return None


def normalize_google_profile_claims(claims: Mapping[str, Any]) -> NormalizedProfileClaims:
    subject = _compact(claims.get("sub"))
    if not subject:
        subject = base64.urlsafe_b64encode(
            hashlib.sha256(json.dumps(dict(claims), sort_keys=True, separators=(",", ":")).encode("utf-8")).digest()
        ).decode("ascii").rstrip("=")
    return NormalizedProfileClaims(
        subject=subject,
        email=_compact(claims.get("email")),
        email_verified=_boolish(claims.get("email_verified")),
        display_name=_compact(claims.get("name")),
        given_name=_compact(claims.get("given_name")),
        family_name=_compact(claims.get("family_name")),
        picture_url=_compact(claims.get("picture")),
        locale=_compact(claims.get("locale")),
        raw_provider="google",
    )


def fetch_google_profile_claims(access_token: str, session: Optional[requests.Session] = None) -> Mapping[str, Any]:
    http = session or requests.Session()
    response = http.get(
        GOOGLE_OIDC_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=float(os.environ.get("GOOGLE_OIDC_TIMEOUT_SECONDS", "10")),
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Google userinfo response must be a JSON object")
    return payload


def fetch_and_normalize_google_profile_claims(access_token: str, session: Optional[requests.Session] = None) -> NormalizedProfileClaims:
    return normalize_google_profile_claims(fetch_google_profile_claims(access_token, session=session))
