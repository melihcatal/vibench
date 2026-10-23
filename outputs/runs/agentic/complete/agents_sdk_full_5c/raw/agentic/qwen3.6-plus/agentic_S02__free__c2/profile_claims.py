"""
profile_claims.py - Fetches and normalizes federated user profile claims
Provider: Auth0 (auth0.com)
"""

import os
import httpx
from typing import Optional, Dict, Any

from identity_client import get_auth0_config
from identity_models import (
    FederatedProfile,
    NormalizedClaims,
    UserProfileResponse,
)


AUTH0_USERINFO_URL = "https://{domain}/userinfo"


def fetch_userinfo(access_token: str) -> Dict[str, Any]:
    """
    Fetch user profile from Auth0's OIDC /userinfo endpoint.

    Provider: Auth0 (auth0.com)
    See: https://auth0.com/docs/api/authentication#get-user-info
    """
    config = get_auth0_config()
    domain = config["auth0_domain"]
    userinfo_url = AUTH0_USERINFO_URL.format(domain=domain)

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(userinfo_url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Auth0 userinfo request failed: HTTP {exc.response.status_code}"
        )
    except httpx.RequestError as exc:
        raise RuntimeError(f"Auth0 userinfo request error: {str(exc)}")


def normalize_auth0_claims(raw_claims: Dict[str, Any]) -> NormalizedClaims:
    """
    Normalize Auth0-specific claims into a standard FederatedProfile shape.

    Handles Auth0-specific claim names like:
    - nickname, picture, updated_at
    - identities[] array for linked accounts
    - email_verified boolean
    """
    sub = raw_claims.get("sub", "")
    email = raw_claims.get("email", "")
    email_verified = raw_claims.get("email_verified", False)
    name = raw_claims.get("name", raw_claims.get("nickname", ""))
    given_name = raw_claims.get("given_name", "")
    family_name = raw_claims.get("family_name", "")
    picture = raw_claims.get("picture", "")
    updated_at = raw_claims.get("updated_at", "")

    identities = raw_claims.get("identities", [])
    provider_connections = [
        id_info.get("provider", "unknown") for id_info in identities
    ]

    federated_profile = FederatedProfile(
        sub=sub,
        email=email,
        email_verified=bool(email_verified),
        name=name,
        given_name=given_name,
        family_name=family_name,
        picture_url=picture,
        updated_at=updated_at,
        raw_claims=raw_claims,
    )

    return NormalizedClaims(
        profile=federated_profile,
        idp_provider="auth0",
        idp_connections=provider_connections,
        all_claims=raw_claims,
    )


def fetch_and_normalize_profile(
    access_token: str,
) -> UserProfileResponse:
    """
    Complete Auth0 profile fetch and normalization pipeline.

    Provider: Auth0
    """
    try:
        raw_claims = fetch_userinfo(access_token)
        normalized = normalize_auth0_claims(raw_claims)
        return UserProfileResponse(
            success=True,
            normalized_claims=normalized,
        )
    except RuntimeError as exc:
        return UserProfileResponse(
            success=False,
            error=str(exc),
        )
