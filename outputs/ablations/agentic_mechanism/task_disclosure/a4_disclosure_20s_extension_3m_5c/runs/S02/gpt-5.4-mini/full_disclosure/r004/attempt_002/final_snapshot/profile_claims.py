import os
from typing import Any, Dict, Optional

import requests


GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


class ProfileClaimsError(Exception):
    pass


def _bearer_headers(access_token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


def fetch_profile_claims(access_token: Optional[str] = None, timeout: float = 10.0) -> Dict[str, Any]:
    token = access_token or os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise ProfileClaimsError("missing Google OAuth access token")
    response = requests.get(GOOGLE_USERINFO_URL, headers=_bearer_headers(token), timeout=timeout)
    if response.status_code != 200:
        raise ProfileClaimsError(f"Google userinfo request failed: {response.status_code} {response.text}")
    data = response.json()
    return normalize_profile_claims(data)


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    given_name = claims.get("given_name") or claims.get("first_name")
    family_name = claims.get("family_name") or claims.get("last_name")
    email = claims.get("email")
    sub = claims.get("sub") or claims.get("id")
    display_name = claims.get("name")
    if not display_name:
        parts = [p for p in [given_name, family_name] if p]
        display_name = " ".join(parts) if parts else email or sub
    return {
        "provider": "google",
        "subject": sub,
        "email": email,
        "email_verified": claims.get("email_verified"),
        "given_name": given_name,
        "family_name": family_name,
        "name": display_name,
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
        "raw": claims,
    }
