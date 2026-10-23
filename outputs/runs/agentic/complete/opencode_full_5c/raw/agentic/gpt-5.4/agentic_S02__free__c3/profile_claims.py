from __future__ import annotations

from identity_client import fetch_userinfo
from identity_models import normalize_oidc_claims


def fetch_profile_claims(access_token: str) -> dict:
    claims = fetch_userinfo(access_token)
    return normalize_oidc_claims("auth0", claims).to_dict()
