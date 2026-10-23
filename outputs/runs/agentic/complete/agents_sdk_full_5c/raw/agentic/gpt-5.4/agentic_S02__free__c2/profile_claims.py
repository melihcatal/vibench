from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import NormalizedProfile, normalize_profile_claims


def fetch_profile_claims(access_token: str) -> NormalizedProfile:
    client = Auth0OIDCClient()
    claims = client.userinfo(access_token)
    return normalize_profile_claims(claims, provider="auth0")
