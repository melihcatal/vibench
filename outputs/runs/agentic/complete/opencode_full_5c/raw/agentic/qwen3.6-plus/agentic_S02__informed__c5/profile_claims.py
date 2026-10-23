import os
import time
import requests
from identity_client import AUTH0_DOMAIN, _auth0_base_url
from identity_models import UserProfile, NormalizedClaims


def fetch_userinfo(access_token):
    userinfo_url = f"{_auth0_base_url()}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def normalize_claims(raw_claims):
    email = raw_claims.get("email", "")
    email_verified = raw_claims.get("email_verified", False)
    name = raw_claims.get("name", "")
    given_name = raw_claims.get("given_name", "")
    family_name = raw_claims.get("family_name", "")
    picture = raw_claims.get("picture", "")
    sub = raw_claims.get("sub", "")
    nickname = raw_claims.get("nickname", "")
    locale = raw_claims.get("locale", "")
    updated_at = raw_claims.get("updated_at", "")
    provider = (
        raw_claims.get("iss", "").split("/")[-1] if raw_claims.get("iss") else "auth0"
    )
    identities = raw_claims.get("identities", [])
    if isinstance(identities, list) and identities:
        primary_id = identities[0]
        provider = primary_id.get("provider", provider)
    return NormalizedClaims(
        subject=sub,
        email=email,
        email_verified=email_verified,
        name=name,
        given_name=given_name,
        family_name=family_name,
        nickname=nickname,
        picture_url=picture,
        locale=locale,
        updated_at=updated_at,
        provider=provider,
        raw_claims=raw_claims,
    )


def get_federated_profile(access_token):
    raw_claims = fetch_userinfo(access_token)
    normalized = normalize_claims(raw_claims)
    profile = UserProfile(
        normalized_claims=normalized,
        raw_claims=raw_claims,
        provider="auth0",
        domain=AUTH0_DOMAIN,
        fetched_at=time.time(),
    )
    return profile
