from __future__ import annotations

from identity_client import fetch_okta_userinfo
from identity_models import NormalizedProfile


def profile_claims(access_token: str) -> dict:
    claims = fetch_okta_userinfo(access_token)
    profile = NormalizedProfile(
        provider="okta",
        subject=claims["sub"],
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        raw=claims,
    )
    return profile.to_dict()
