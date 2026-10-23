from __future__ import annotations

from identity_client import fetch_userinfo, load_auth0_settings
from identity_models import FederatedProfile, normalize_bool


def fetch_profile_claims(access_token: str) -> FederatedProfile:
    settings = load_auth0_settings()
    raw = fetch_userinfo(access_token)
    return FederatedProfile(
        subject=str(raw["sub"]),
        email=raw.get("email"),
        email_verified=normalize_bool(raw.get("email_verified")),
        name=raw.get("name"),
        given_name=raw.get("given_name"),
        family_name=raw.get("family_name"),
        picture=raw.get("picture"),
        locale=raw.get("locale"),
        provider=f"auth0:{settings.domain}",
        raw=raw,
    )
