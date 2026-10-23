import json
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


class ProfileClaimsError(Exception):
    pass


def _pick_string(data: Dict[str, Any], *keys: str) -> Optional[str]:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    email = _pick_string(claims, "email", "preferred_username")
    given_name = _pick_string(claims, "given_name", "first_name")
    family_name = _pick_string(claims, "family_name", "last_name")
    name = _pick_string(claims, "name", "full_name")
    picture = _pick_string(claims, "picture", "avatar_url")
    user_id = _pick_string(claims, "sub", "id", "user_id")

    normalized_name = name
    if not normalized_name and (given_name or family_name):
        normalized_name = " ".join(part for part in [given_name, family_name] if part)

    return {
        "provider": "google",
        "id": user_id,
        "email": email,
        "name": normalized_name,
        "given_name": given_name,
        "family_name": family_name,
        "picture": picture,
        "locale": _pick_string(claims, "locale"),
        "raw": claims,
    }


def fetch_google_profile_claims(access_token: Optional[str] = None, timeout: float = 10.0) -> Dict[str, Any]:
    token = access_token or os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise ProfileClaimsError("Missing Google OAuth access token")

    response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )

    if response.status_code != 200:
        raise ProfileClaimsError(f"Google userinfo request failed: {response.status_code} {response.text}")

    try:
        claims = response.json()
    except json.JSONDecodeError as exc:
        raise ProfileClaimsError("Invalid JSON returned by Google userinfo endpoint") from exc

    if not isinstance(claims, dict):
        raise ProfileClaimsError("Google userinfo response was not a JSON object")

    return normalize_profile_claims(claims)
