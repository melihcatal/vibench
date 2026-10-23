from __future__ import annotations

from identity_client import Auth0OIDCClient, load_auth0_config
from identity_models import NormalizedProfile, coerce_bool


def fetch_profile_claims(access_token: str) -> NormalizedProfile:
    client = Auth0OIDCClient(load_auth0_config())
    raw = client.fetch_userinfo(access_token)
    return NormalizedProfile(
        subject=raw["sub"],
        email=raw.get("email"),
        email_verified=coerce_bool(raw.get("email_verified")),
        name=raw.get("name"),
        given_name=raw.get("given_name"),
        family_name=raw.get("family_name"),
        picture=raw.get("picture"),
        locale=raw.get("locale"),
        updated_at=str(raw.get("updated_at")) if raw.get("updated_at") is not None else None,
        provider="auth0",
        raw=raw,
    )
