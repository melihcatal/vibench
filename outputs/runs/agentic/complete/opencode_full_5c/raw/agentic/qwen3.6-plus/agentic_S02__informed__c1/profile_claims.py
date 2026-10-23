import os
from typing import Optional, List

from identity_models import OAuthConfig, UserProfile, normalize_claims
from identity_client import fetch_user_info, load_oauth_config


CLAIM_PRIORITY_ORDER = [
    "sub",
    "email",
    "name",
    "given_name",
    "family_name",
    "nickname",
    "picture",
    "locale",
    "email_verified",
    "updated_at",
    "phone_number",
    "address",
    "zoneinfo",
]


def fetch_profile_claims(
    access_token: str,
    redirect_uri: Optional[str] = None,
) -> UserProfile:
    config = load_oauth_config(redirect_uri=redirect_uri)
    return fetch_user_info(config=config, access_token=access_token)


def normalize_profile_claims(
    raw_claims: dict,
    provider: str = "auth0",
) -> UserProfile:
    return normalize_claims(raw_claims, provider=provider)


def extract_standard_claims(
    raw_claims: dict,
) -> dict:
    standard_claims = {}
    for claim in CLAIM_PRIORITY_ORDER:
        if claim in raw_claims:
            standard_claims[claim] = raw_claims[claim]
    return standard_claims


def extract_custom_claims(
    raw_claims: dict,
    namespace: str = "https://",
) -> dict:
    custom_claims = {}
    for key, value in raw_claims.items():
        if key.startswith(namespace) or key not in CLAIM_PRIORITY_ORDER:
            custom_claims[key] = value
    return custom_claims


def merge_profiles(
    primary: UserProfile,
    secondary_claims: dict,
) -> UserProfile:
    merged = primary.raw_claims.copy()
    for key, value in secondary_claims.items():
        if key not in merged or not merged[key]:
            merged[key] = value

    return normalize_claims(merged, provider=primary.provider)


def get_claims_for_scopes(
    raw_claims: dict,
    requested_scopes: List[str],
) -> dict:
    scope_claim_map = {
        "openid": ["sub"],
        "profile": [
            "name",
            "given_name",
            "family_name",
            "nickname",
            "picture",
            "locale",
            "updated_at",
        ],
        "email": ["email", "email_verified"],
        "phone": ["phone_number", "phone_number_verified"],
        "address": ["address"],
    }

    allowed_claims = set()
    for scope in requested_scopes:
        if scope in scope_claim_map:
            allowed_claims.update(scope_claim_map[scope])

    return {k: v for k, v in raw_claims.items() if k in allowed_claims}


def validate_required_claims(
    profile: UserProfile,
    required_fields: Optional[List[str]] = None,
) -> tuple:
    if required_fields is None:
        required_fields = ["sub", "email"]

    missing = []
    for field in required_fields:
        value = getattr(profile, field, None)
        if not value:
            missing.append(field)

    is_valid = len(missing) == 0
    return is_valid, missing


def format_display_name(profile: UserProfile) -> str:
    if profile.name:
        return profile.name
    if profile.given_name and profile.family_name:
        return f"{profile.given_name} {profile.family_name}"
    if profile.given_name:
        return profile.given_name
    if profile.nickname:
        return profile.nickname
    if profile.email:
        return profile.email
    return profile.sub


def build_identity_assertion(
    profile: UserProfile,
    audience: str = "",
    issuer: str = "auth0",
) -> dict:
    return {
        "iss": f"https://{issuer}/",
        "sub": profile.sub,
        "aud": audience,
        "email": profile.email,
        "email_verified": profile.email_verified,
        "name": profile.name,
        "preferred_username": profile.nickname or profile.email,
        "picture": profile.picture,
        "locale": profile.locale,
        "updated_at": profile.updated_at,
        "provider": "auth0",
    }
