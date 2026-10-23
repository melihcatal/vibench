from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import NormalizedProfile, normalize_auth0_profile


def fetch_and_normalize_profile(access_token: str) -> NormalizedProfile:
    client = Auth0OIDCClient()
    claims = client.fetch_userinfo(access_token)
    return normalize_auth0_profile(claims)
