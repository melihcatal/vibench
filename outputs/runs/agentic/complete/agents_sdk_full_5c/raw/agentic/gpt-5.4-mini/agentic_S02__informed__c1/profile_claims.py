from __future__ import annotations

from identity_client import fetch_userinfo, load_identity_config
from identity_models import NormalizedProfile, normalize_claims


def fetch_and_normalize_profile(access_token: str) -> NormalizedProfile:
    config = load_identity_config("AUTH0")
    claims = fetch_userinfo(config, access_token)
    return normalize_claims(claims, provider="auth0")
