from __future__ import annotations

from identity_client import fetch_userinfo, load_auth0_settings
from identity_models import NormalizedProfile, normalize_auth0_profile


PROVIDER = "Auth0 Authentication API"



def fetch_and_normalize_profile_claims(access_token: str) -> NormalizedProfile:
    settings = load_auth0_settings()
    claims = fetch_userinfo(settings, access_token)
    return normalize_auth0_profile(claims)
