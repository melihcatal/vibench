import os
from typing import Any, Dict, Optional

import requests


GOOGLE_OIDC_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def _coalesce(value: Optional[Any]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value)


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Optional[str]]:
    return {
        "issuer": _coalesce(claims.get("iss")),
        "subject": _coalesce(claims.get("sub")),
        "email": _coalesce(claims.get("email")),
        "email_verified": _coalesce(claims.get("email_verified")),
        "full_name": _coalesce(claims.get("name")),
        "given_name": _coalesce(claims.get("given_name")),
        "family_name": _coalesce(claims.get("family_name")),
        "avatar_url": _coalesce(claims.get("picture")),
        "locale": _coalesce(claims.get("locale")),
        "provider": "google",
    }


def fetch_google_profile_claims(access_token: Optional[str] = None, timeout: int = 10) -> Dict[str, Optional[str]]:
    token = access_token or os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing Google OAuth access token")

    response = requests.get(
        GOOGLE_OIDC_USERINFO_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json())
