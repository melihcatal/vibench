"""
profile_claims.py - Fetches and normalizes federated user profile claims
from the Auth0 /userinfo endpoint.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from identity_client import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    fetch_userinfo,
)
from identity_models import UserProfile, normalize_profile

logger = logging.getLogger(__name__)


def fetch_and_normalize_profile(
    access_token: str,
    domain: str = AUTH0_DOMAIN,
) -> UserProfile:
    """
    Fetch the user's profile from Auth0's userinfo endpoint and normalize
    the claims into a UserProfile.
    """
    raw_claims = fetch_userinfo(access_token, domain=domain)
    profile = normalize_profile(raw_claims)
    logger.info(
        "Fetched profile for sub=%s, email=%s from auth0",
        profile.subject,
        profile.email,
    )
    return profile


def extract_federated_identities(profile: UserProfile) -> list[dict[str, Any]]:
    """Extract linked federated identity records from Auth0 profile."""
    identities = profile.raw_claims.get("identities", [])
    return [
        {
            "provider": idp.get("provider"),
            "connection": idp.get("connection"),
            "user_id": idp.get("user_id"),
            "is_social": idp.get("isSocial", False),
        }
        for idp in identities
    ]


def get_profile_summary(profile: UserProfile) -> dict[str, str | bool | list]:
    """Return a concise summary of the federated profile."""
    return {
        "subject": profile.subject,
        "email": profile.email or "",
        "email_verified": profile.email_verified,
        "name": profile.name or "",
        "federated_providers": [
            idp["provider"] for idp in extract_federated_identities(profile)
        ],
    }


if __name__ == "__main__":
    sample_claims = {
        "sub": "auth0|5f8a1b2c3d4e5f0012345678",
        "email": "user@example.com",
        "email_verified": True,
        "name": "Jane Doe",
        "given_name": "Jane",
        "family_name": "Doe",
        "picture": "https://example.com/avatar.png",
        "updated_at": "2024-01-15T10:30:00.000Z",
        "identities": [
            {
                "provider": "google-oauth2",
                "connection": "google-oauth2",
                "user_id": "112233445566",
                "isSocial": True,
            }
        ],
    }
    profile = normalize_profile(sample_claims)
    print(json.dumps(get_profile_summary(profile), indent=2))
