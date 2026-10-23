from __future__ import annotations

from identity_client import IdentityClient

GOOGLE_OIDC_PROVIDER = "Google OIDC UserInfo"


def profile_claims(access_token: str) -> dict:
    client = IdentityClient()
    profile = client.normalized_profile(access_token)
    return profile.__dict__
