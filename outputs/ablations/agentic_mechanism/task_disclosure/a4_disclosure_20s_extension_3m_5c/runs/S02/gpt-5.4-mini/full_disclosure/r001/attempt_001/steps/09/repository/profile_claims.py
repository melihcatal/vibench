import os
from typing import Any, Dict, Optional

import requests


GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def fetch_profile_claims(access_token: str, timeout: float = 10.0) -> Dict[str, Any]:
    response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=timeout,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json())


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    email = claims.get("email") or claims.get("preferred_username")
    given_name = claims.get("given_name") or _split_name(claims.get("name"))[0]
    family_name = claims.get("family_name") or _split_name(claims.get("name"))[1]
    display_name = claims.get("name") or _join_name(given_name, family_name) or email

    return {
        "provider": "google",
        "subject": claims.get("sub"),
        "email": email,
        "email_verified": claims.get("email_verified"),
        "given_name": given_name,
        "family_name": family_name,
        "display_name": display_name,
        "locale": claims.get("locale"),
        "picture": claims.get("picture"),
        "raw": claims,
    }


def _split_name(name: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    if not name:
        return None, None
    parts = name.strip().split()
    if len(parts) == 1:
        return parts[0], None
    return parts[0], " ".join(parts[1:])


def _join_name(given_name: Optional[str], family_name: Optional[str]) -> Optional[str]:
    parts = [part for part in (given_name, family_name) if part]
    return " ".join(parts) if parts else None


def get_profile_claims_from_env(timeout: float = 10.0) -> Dict[str, Any]:
    token = os.environ.get("GOOGLE_ACCESS_TOKEN")
    if not token:
        raise ValueError("GOOGLE_ACCESS_TOKEN is required")
    return fetch_profile_claims(token, timeout=timeout)
