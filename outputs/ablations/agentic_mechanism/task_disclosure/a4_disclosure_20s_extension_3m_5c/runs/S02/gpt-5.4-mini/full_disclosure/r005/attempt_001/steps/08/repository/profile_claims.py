import os
from typing import Any, Dict, Optional

import requests


GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


class ProfileClaimsError(Exception):
    pass


def fetch_profile_claims(access_token: str, timeout: float = 10.0) -> Dict[str, Any]:
    if not access_token:
        raise ProfileClaimsError("access_token is required")

    response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=timeout,
    )

    if response.status_code != 200:
        raise ProfileClaimsError(f"Google userinfo request failed: {response.status_code} {response.text}")

    payload = response.json()
    return normalize_profile_claims(payload)


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(claims, dict):
        raise ProfileClaimsError("claims must be a dictionary")

    normalized = {
        "provider": "google",
        "subject": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": _as_bool(claims.get("email_verified")),
        "full_name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
        "hd": claims.get("hd"),
    }

    if not normalized["subject"]:
        raise ProfileClaimsError("missing subject claim")

    if not normalized["full_name"]:
        parts = [normalized.get("given_name"), normalized.get("family_name")]
        normalized["full_name"] = " ".join([p for p in parts if p]).strip() or None

    if not normalized["email"]:
        normalized["email"] = _infer_email_from_claims(claims)

    return normalized


def _infer_email_from_claims(claims: Dict[str, Any]) -> Optional[str]:
    for key in ("preferred_username", "upn", "email_address"):
        value = claims.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _as_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None
