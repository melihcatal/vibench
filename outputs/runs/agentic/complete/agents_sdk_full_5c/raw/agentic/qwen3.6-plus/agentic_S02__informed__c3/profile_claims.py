"""Fetch and normalize federated user profile claims using Google Identity Platform."""

import time
from typing import Optional, Dict, Any

import requests

from identity_client import IdentityClient, GoogleOIDCConfig
from identity_models import UserProfileClaims


def fetch_user_profile(
    access_token: str,
    token_type: str = "Bearer",
) -> Dict[str, Any]:
    """
    Fetch the user's profile claims from Google's OpenID Connect userinfo endpoint.
    """
    headers = {
        "Authorization": f"{token_type} {access_token}",
        "Accept": "application/json",
    }
    response = requests.get(
        GoogleOIDCConfig.USERINFO_ENDPOINT,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def normalize_claims(
    raw_claims: Dict[str, Any],
    access_token: str,
    id_token: Optional[str] = None,
) -> UserProfileClaims:
    """
    Normalize raw claims from Google Identity Platform into a standardized UserProfileClaims.
    """
    profile = UserProfileClaims.from_oidc_claims(
        raw_claims,
        provider="Google Identity Platform",
    )
    return profile


def fetch_and_normalize_profile(
    access_token: str,
    token_type: str = "Bearer",
    id_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch profile claims from Google OIDC userinfo endpoint and normalize them.
    Returns a structured dict with the normalized claims.
    """
    raw_claims = fetch_user_profile(access_token, token_type)
    normalized = normalize_claims(raw_claims, access_token, id_token)

    return {
        "sub": normalized.sub,
        "email": normalized.email,
        "email_verified": normalized.email_verified,
        "name": normalized.name,
        "given_name": normalized.given_name,
        "family_name": normalized.family_name,
        "picture": normalized.picture,
        "locale": normalized.locale,
        "preferred_username": normalized.preferred_username,
        "provider": normalized.provider,
        "normalized_at": time.time(),
    }


def get_full_user_profile(
    access_token: str,
    id_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function to get a full normalized user profile from Google Identity Platform.
    """
    try:
        return fetch_and_normalize_profile(access_token, id_token=id_token)
    except requests.RequestException as exc:
        return {
            "error": "profile_fetch_failed",
            "message": str(exc),
            "provider": GoogleOIDCConfig.PROVIDER_NAME,
        }


if __name__ == "__main__":
    import os

    demo_token = os.environ.get("DEMO_ACCESS_TOKEN", "")
    if demo_token:
        profile = get_full_user_profile(demo_token)
        print("User profile:", profile)
    else:
        print("Set DEMO_ACCESS_TOKEN env var to test profile fetching.")
