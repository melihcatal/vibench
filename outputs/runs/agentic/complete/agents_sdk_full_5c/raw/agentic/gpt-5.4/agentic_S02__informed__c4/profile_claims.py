from __future__ import annotations

from identity_client import fetch_userinfo



def fetch_and_normalize_profile_claims(access_token: str) -> dict:
    profile = fetch_userinfo(access_token)
    return {
        "provider": "Auth0 Authentication API",
        "sub": profile.sub,
        "email": profile.email,
        "email_verified": profile.email_verified,
        "name": profile.name,
        "given_name": profile.given_name,
        "family_name": profile.family_name,
        "picture": profile.picture,
        "locale": profile.locale,
        "updated_at": profile.updated_at,
        "raw": profile.raw,
    }
