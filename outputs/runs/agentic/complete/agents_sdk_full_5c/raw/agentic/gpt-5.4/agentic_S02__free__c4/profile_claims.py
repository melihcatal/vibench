from __future__ import annotations

from identity_client import Auth0Client
from identity_models import NormalizedProfile


def fetch_profile_claims(access_token: str, client: Auth0Client | None = None) -> NormalizedProfile:
    auth0 = client or Auth0Client()
    claims = auth0.userinfo(access_token)
    return NormalizedProfile(
        provider="Auth0",
        subject=claims["sub"],
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        raw_claims=claims,
    )
