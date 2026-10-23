"""
Fetch and normalize federated user profile claims from Auth0 /userinfo endpoint.
Extracts standardized claims and maps Auth0-specific fields to a common profile schema.
"""

import os
import asyncio
from typing import Optional, Dict, Any, List

from identity_client import create_auth0_client, AUTH0_DOMAIN
from identity_models import FederatedProfile, normalize_email, extract_provider_from_sub


class ProfileFetchError(Exception):
    """Raised when fetching the user profile fails."""
    pass


CLAIM_MAPPING = {
    "sub": "sub",
    "email": "email",
    "email_verified": "email_verified",
    "name": "name",
    "given_name": "given_name",
    "family_name": "family_name",
    "nickname": "nickname",
    "picture": "picture",
    "locale": "locale",
    "updated_at": "updated_at",
    "zoneinfo": "timezone",
    "phone_number": "phone",
    "phone_number_verified": "phone_verified",
    "address": "address",
}


def map_auth0_claims(raw_claims: Dict[str, Any]) -> Dict[str, Any]:
    """Map Auth0-specific claims to normalized profile fields."""
    mapped = {}
    for auth0_key, normalized_key in CLAIM_MAPPING.items():
        if auth0_key in raw_claims:
            mapped[normalized_key] = raw_claims[auth0_key]
    return mapped


def enrich_profile_with_metadata(
    profile: FederatedProfile,
    raw_claims: Dict[str, Any],
) -> FederatedProfile:
    """Enrich the normalized profile with derived metadata."""
    profile.email = normalize_email(profile.email)
    profile.provider = extract_provider_from_sub(profile.sub)

    auth0_metadata = raw_claims.get("https://dev-example.auth0.com/user_metadata", {})
    if auth0_metadata:
        profile.raw_claims["user_metadata"] = auth0_metadata

    app_metadata = raw_claims.get("https://dev-example.auth0.com/app_metadata", {})
    if app_metadata:
        profile.raw_claims["app_metadata"] = app_metadata

    return profile


async def fetch_user_profile(
    access_token: str,
    domain: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch user profile from Auth0 /userinfo endpoint.

    Returns normalized profile with raw claims preserved.
    """
    client = create_auth0_client(
        domain=domain or os.getenv("AUTH0_DOMAIN", AUTH0_DOMAIN),
    )

    try:
        raw_claims = await client.get_userinfo(access_token)
    except Exception as exc:
        raise ProfileFetchError(f"Failed to fetch profile from Auth0: {exc}") from exc

    profile = FederatedProfile.from_auth0_userinfo(raw_claims)
    profile = enrich_profile_with_metadata(profile, raw_claims)

    return {
        "profile": profile,
        "raw_claims": raw_claims,
        "normalized_claims": map_auth0_claims(raw_claims),
        "provider": "auth0",
        "domain": client.domain,
    }


async def fetch_and_validate_profile(
    access_token: str,
    required_claims: Optional[List[str]] = None,
    domain: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch profile and validate required claims are present.
    Raises ProfileFetchError if required claims are missing.
    """
    result = await fetch_user_profile(access_token, domain=domain)
    profile = result["profile"]

    required = required_claims or ["sub", "email"]
    missing = []
    for claim in required:
        value = getattr(profile, claim, None)
        if not value:
            missing.append(claim)

    if missing:
        raise ProfileFetchError(
            f"Missing required claims from Auth0 profile: {', '.join(missing)}"
        )

    return result


def format_profile_response(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format profile result for API response."""
    profile = result["profile"]
    return {
        "sub": profile.sub,
        "email": profile.email,
        "email_verified": profile.email_verified,
        "name": profile.name,
        "given_name": profile.given_name,
        "family_name": profile.family_name,
        "picture": profile.picture,
        "provider": profile.provider,
        "locale": profile.locale,
    }


if __name__ == "__main__":
    async def main():
        try:
            result = await fetch_user_profile("sample_access_token")
            print(f"Profile fetched for: {result['profile'].email}")
        except ProfileFetchError as e:
            print(f"Profile fetch error: {e}")

    asyncio.run(main())
