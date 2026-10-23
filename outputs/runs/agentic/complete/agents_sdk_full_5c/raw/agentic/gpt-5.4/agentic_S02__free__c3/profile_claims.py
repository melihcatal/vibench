from __future__ import annotations

from identity_client import Auth0Client, load_auth0_config
from identity_models import FederatedProfile, normalize_auth0_profile


def fetch_profile_claims(access_token: str) -> dict:
    client = Auth0Client(load_auth0_config(public_client=False))
    return client.fetch_userinfo(access_token)


def normalized_profile(access_token: str) -> FederatedProfile:
    claims = fetch_profile_claims(access_token)
    return normalize_auth0_profile(claims)
