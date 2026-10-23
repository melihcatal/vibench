from __future__ import annotations

from typing import Dict

from identity_client import fetch_userinfo
from identity_models import FederatedProfile, normalize_claims


def fetch_and_normalize_profile(access_token: str) -> FederatedProfile:
    claims: Dict[str, object] = fetch_userinfo(access_token)
    profile = normalize_claims(claims)
    return profile
