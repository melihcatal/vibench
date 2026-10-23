from __future__ import annotations

from identity_client import fetch_userinfo, load_identity_config
from identity_models import normalize_profile_claims


def fetch_and_normalize_profile(access_token: str):
    config = load_identity_config()
    claims = fetch_userinfo(config, access_token)
    return normalize_profile_claims(claims, issuer=config.issuer)
