from __future__ import annotations

from identity_client import GOOGLE_USERINFO_URL, fetch_google_userinfo
from identity_models import FederatedProfile, normalize_profile


def fetch_profile_claims(access_token: str) -> FederatedProfile:
    claims = fetch_google_userinfo(access_token)
    profile = normalize_profile("google_oidc", claims)
    profile.raw["userinfo_endpoint"] = GOOGLE_USERINFO_URL
    return profile
