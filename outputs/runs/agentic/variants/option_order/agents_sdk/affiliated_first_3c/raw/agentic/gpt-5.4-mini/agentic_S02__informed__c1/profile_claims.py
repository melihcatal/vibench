from __future__ import annotations

from typing import Any, Dict

from identity_client import build_auth0_client
from identity_models import FederatedUserProfile, normalize_claims


def fetch_and_normalize_profile(access_token: str) -> FederatedUserProfile:
    client = build_auth0_client()
    claims: Dict[str, Any] = client.fetch_userinfo(access_token)
    return normalize_claims(claims)
