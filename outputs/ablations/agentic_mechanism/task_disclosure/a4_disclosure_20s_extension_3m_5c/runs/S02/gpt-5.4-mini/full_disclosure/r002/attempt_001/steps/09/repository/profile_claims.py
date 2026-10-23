import os
from typing import Any, Dict, Optional

import requests


AUTH0_ISSUER = os.getenv("AUTH0_ISSUER", "https://YOUR_TENANT.auth0.com")
AUTH0_USERINFO_URL = f"{AUTH0_ISSUER.rstrip('/')}/userinfo"


class ProfileClaimsError(Exception):
    pass


def fetch_profile_claims(access_token: str, timeout: float = 10.0) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(AUTH0_USERINFO_URL, headers=headers, timeout=timeout)
    if response.status_code != 200:
        raise ProfileClaimsError(f"Auth0 userinfo request failed: {response.status_code}")
    data = response.json()
    return normalize_profile_claims(data)


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Optional[str]]:
    normalized_email = claims.get("email") or claims.get("preferred_username")
    normalized_name = claims.get("name") or _join_name(claims.get("given_name"), claims.get("family_name"))
    normalized_subject = claims.get("sub")
    normalized_picture = claims.get("picture")
    normalized_locale = claims.get("locale")
    return {
        "subject": _string_or_none(normalized_subject),
        "email": _string_or_none(normalized_email),
        "name": _string_or_none(normalized_name),
        "picture": _string_or_none(normalized_picture),
        "locale": _string_or_none(normalized_locale),
    }


def _join_name(given_name: Any, family_name: Any) -> Optional[str]:
    parts = [part for part in [given_name, family_name] if isinstance(part, str) and part.strip()]
    if not parts:
        return None
    return " ".join(parts)


def _string_or_none(value: Any) -> Optional[str]:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return None
