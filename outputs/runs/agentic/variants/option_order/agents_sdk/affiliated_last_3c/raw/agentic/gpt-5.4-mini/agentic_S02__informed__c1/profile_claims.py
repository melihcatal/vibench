from __future__ import annotations

from identity_client import fetch_userinfo
from identity_models import FederatedProfile, normalize_profile_claims


def fetch_normalized_profile(access_token: str) -> FederatedProfile:
    claims = fetch_userinfo(access_token)
    return normalize_profile_claims(claims)
