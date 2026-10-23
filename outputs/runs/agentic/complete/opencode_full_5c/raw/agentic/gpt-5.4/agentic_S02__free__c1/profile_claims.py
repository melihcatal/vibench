from __future__ import annotations

from identity_client import fetch_auth0_userinfo
from identity_models import normalize_auth0_profile


def profile_claims(access_token: str) -> dict:
    profile = fetch_auth0_userinfo(access_token)
    return normalize_auth0_profile(profile).to_dict()
