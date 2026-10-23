from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import FederatedProfile, normalize_profile


def fetch_profile_claims(access_token: str) -> FederatedProfile:
    client = Auth0OIDCClient()
    claims = client.fetch_userinfo(access_token)
    return normalize_profile("Auth0", claims)
