from __future__ import annotations

from identity_client import fetch_userinfo
from identity_models import normalize_profile, to_dict


def profile_claims(access_token: str) -> dict:
    claims = fetch_userinfo(access_token)
    normalized = normalize_profile(claims)
    payload = to_dict(normalized)
    payload["provider"] = "auth0"
    return payload
