from __future__ import annotations

from identity_client import Auth0Client
from identity_models import NormalizedProfile, normalize_auth0_profile


def fetch_profile_claims(access_token: str) -> dict:
    client = Auth0Client()
    return client.fetch_userinfo(access_token)


def normalize_profile_claims(access_token: str) -> NormalizedProfile:
    raw_claims = fetch_profile_claims(access_token)
    return normalize_auth0_profile(raw_claims)
