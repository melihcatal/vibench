"""Fetch and normalize federated user profile claims from Auth0.

This module retrieves the user profile from the Auth0 /userinfo endpoint
using the access token and normalizes the claims into a standard UserProfile.

Provider: Auth0 Authentication API
SDK: requests
Auth env vars: AUTH0_DOMAIN
"""

import os
import requests
from typing import Optional, Dict, Any

from identity_client import AUTH0_USERINFO_ENDPOINT
from identity_models import UserProfile


def fetch_user_profile(
    access_token: str,
    token_type: str = "Bearer",
) -> UserProfile:
    """Fetch and normalize federated user profile from Auth0 /userinfo endpoint.

    Args:
        access_token: The OAuth2 access token obtained during login.
        token_type: The token type (default: 'Bearer').

    Returns:
        UserProfile with normalized federated identity claims.

    Raises:
        ValueError: If AUTH0_DOMAIN is not configured.
        requests.RequestException: If the userinfo request fails.
    """
    if not AUTH0_USERINFO_ENDPOINT:
        raise ValueError("AUTH0_DOMAIN environment variable is not set")

    headers = {
        "Authorization": f"{token_type} {access_token}",
        "Accept": "application/json",
    }

    response = requests.get(
        AUTH0_USERINFO_ENDPOINT,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    userinfo = response.json()
    return UserProfile.from_auth0_userinfo(userinfo)


def fetch_user_profile_with_custom_headers(
    access_token: str,
    extra_headers: Optional[Dict[str, str]] = None,
) -> UserProfile:
    """Fetch user profile with additional custom headers for Auth0.

    Args:
        access_token: The OAuth2 access token.
        extra_headers: Additional HTTP headers for the request.

    Returns:
        UserProfile with normalized claims.
    """
    if not AUTH0_USERINFO_ENDPOINT:
        raise ValueError("AUTH0_DOMAIN environment variable is not set")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)

    response = requests.get(
        AUTH0_USERINFO_ENDPOINT,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    return UserProfile.from_auth0_userinfo(response.json())


def extract_normalized_claims(
    access_token: str,
    include_raw: bool = False,
) -> Dict[str, Any]:
    """Extract normalized claims from Auth0 user profile.

    Args:
        access_token: The OAuth2 access token.
        include_raw: Whether to include raw claims in the response.

    Returns:
        Dictionary with normalized user claims.
    """
    profile = fetch_user_profile(access_token)

    claims = {
        "sub": profile.subject,
        "email": profile.email,
        "email_verified": profile.email_verified,
        "name": profile.name,
        "given_name": profile.given_name,
        "family_name": profile.family_name,
        "picture": profile.picture,
        "nickname": profile.nickname,
        "identities": profile.identities,
        "updated_at": profile.updated_at,
    }

    if include_raw:
        claims["raw_claims"] = profile.raw_claims

    return claims


if __name__ == "__main__":
    import sys
    token = sys.argv[1] if len(sys.argv) > 1 else "demo_token"
    try:
        profile = fetch_user_profile(token)
        print(f"Subject: {profile.subject}")
        print(f"Email: {profile.email}")
    except Exception as e:
        print(f"Error: {e}")
