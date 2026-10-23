import os
import requests
from identity_client import load_auth0_config
from identity_models import NormalizedUserProfile


def fetch_userinfo(access_token: str) -> dict:
    config = load_auth0_config()
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    userinfo_endpoint = f"https://{auth0_domain}/userinfo"
    response = requests.get(
        userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def normalize_claims(raw_claims: dict) -> NormalizedUserProfile:
    profile = NormalizedUserProfile.from_claims(raw_claims)
    if not profile.name and profile.given_name and profile.family_name:
        profile.name = f"{profile.given_name} {profile.family_name}"
    if profile.email:
        profile.email = profile.email.strip().lower()
    if profile.phone_number:
        profile.phone_number = profile.phone_number.strip()
    return profile


def fetch_and_normalize_profile(access_token: str) -> NormalizedUserProfile:
    raw_claims = fetch_userinfo(access_token)
    return normalize_claims(raw_claims)


def extract_provider_specific_claims(raw_claims: dict) -> dict:
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    provider_claims = {
        "provider": "auth0",
        "issuer": f"https://{auth0_domain}/",
        "sub": raw_claims.get("sub", ""),
        "email": raw_claims.get("email"),
        "email_verified": raw_claims.get("email_verified", False),
        "name": raw_claims.get("name"),
        "nickname": raw_claims.get("nickname"),
        "picture": raw_claims.get("picture"),
        "updated_at": raw_claims.get("updated_at"),
        "identities": raw_claims.get("identities", []),
        "app_metadata": raw_claims.get("app_metadata", {}),
        "user_metadata": raw_claims.get("user_metadata", {}),
    }
    return provider_claims


def get_federated_profile(
    access_token: str,
    include_raw: bool = False,
) -> dict:
    raw_claims = fetch_userinfo(access_token)
    normalized = normalize_claims(raw_claims)
    result = {
        "sub": normalized.sub,
        "email": normalized.email,
        "email_verified": normalized.email_verified,
        "name": normalized.name,
        "given_name": normalized.given_name,
        "family_name": normalized.family_name,
        "picture": normalized.picture,
        "locale": normalized.locale,
        "phone_number": normalized.phone_number,
    }
    if include_raw:
        result["raw_claims"] = raw_claims
    return result
