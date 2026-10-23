import json
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_OIDC_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def fetch_google_profile_claims(access_token: Optional[str] = None, userinfo_url: str = GOOGLE_OIDC_USERINFO_URL) -> Dict[str, Any]:
    token = access_token or _env("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing Google OAuth access token")

    response = requests.get(
        userinfo_url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    response.raise_for_status()
    claims = response.json()
    return normalize_google_profile_claims(claims)


def normalize_google_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    email = claims.get("email")
    email_verified = claims.get("email_verified")
    subject = claims.get("sub")
    given_name = claims.get("given_name") or claims.get("first_name")
    family_name = claims.get("family_name") or claims.get("last_name")
    full_name = claims.get("name")
    if not full_name and (given_name or family_name):
        full_name = " ".join(part for part in [given_name, family_name] if part)
    picture = claims.get("picture")
    locale = claims.get("locale")

    return {
        "provider": "google",
        "subject": subject,
        "email": email,
        "email_verified": bool(email_verified) if email_verified is not None else None,
        "given_name": given_name,
        "family_name": family_name,
        "name": full_name,
        "picture": picture,
        "locale": locale,
        "raw": claims,
    }


def parse_google_profile_claims(payload: str) -> Dict[str, Any]:
    return normalize_google_profile_claims(json.loads(payload))
