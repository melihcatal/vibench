from __future__ import annotations

from identity_client import AUTH0_PROVIDER, fetch_userinfo
from identity_models import normalize_claims


def profile_claims(access_token: str) -> dict:
    claims = fetch_userinfo(access_token)
    return normalize_claims(AUTH0_PROVIDER, claims).to_dict()
