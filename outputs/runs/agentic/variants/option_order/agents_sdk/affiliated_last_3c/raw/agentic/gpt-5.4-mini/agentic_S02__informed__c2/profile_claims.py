from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import FederatedProfile, normalize_profile_claims


def fetch_and_normalize_profile(access_token: str) -> FederatedProfile:
    client = Auth0IdentityClient()
    profile = client.fetch_userinfo(access_token)
    return normalize_profile_claims(profile.raw)
