from __future__ import annotations

from identity_client import fetch_google_userinfo
from identity_models import normalize_google_claims


def fetch_profile_claims(access_token: str) -> dict:
    claims = fetch_google_userinfo(access_token)
    normalized = normalize_google_claims(claims)
    return {
        "provider": "Google Identity Platform OIDC",
        "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
        "profile": normalized.to_dict(),
    }
