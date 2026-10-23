"""
Fetch and normalize federated user profile claims using Okta's OIDC userinfo endpoint.

Provider: Okta OIDC Userinfo API (https://developer.okta.com/docs/reference/api/oidc/#userinfo)
"""

import os
import time
from typing import Optional
from dataclasses import dataclass, field

import requests
from identity_models import (
    FederatedUserClaims,
    ClaimNormalizationResult,
    normalize_email,
    normalize_name,
)


OKTA_ORG_URL = os.getenv("OKTA_ORG_URL", "https://dev-123456.okta.com")
OKTA_AUTH_SERVER_ID = os.getenv("OKTA_AUTH_SERVER_ID", "default")

# Okta OIDC userinfo endpoint
USERINFO_ENDPOINT = f"{OKTA_ORG_URL}/oauth2/{OKTA_AUTH_SERVER_ID}/v1/userinfo"


class OktaUserinfoError(Exception):
    """Raised when Okta userinfo fetch fails."""
    pass


def fetch_userinfo(access_token: str, timeout: int = 15) -> dict:
    """
    Fetch user profile claims from Okta OIDC /userinfo endpoint.

    Uses the access_token as Bearer token per OIDC specification.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    response = requests.get(USERINFO_ENDPOINT, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise OktaUserinfoError(
            f"Okta userinfo fetch failed: {response.status_code} - {response.text}"
        )

    return response.json()


def normalize_okta_claims(raw_claims: dict) -> FederatedUserClaims:
    """
    Normalize Okta-specific claims to a standard federated user profile.

    Maps Okta claim names to internal standardized field names.
    """
    sub = raw_claims.get("sub", "")
    email = normalize_email(raw_claims.get("email", ""))
    email_verified = raw_claims.get("email_verified", False)

    given_name = raw_claims.get("given_name", "")
    family_name = raw_claims.get("family_name", "")
    full_name = normalize_name(
        given_name=given_name,
        family_name=family_name,
        fallback=raw_claims.get("name", ""),
    )

    preferred_username = raw_claims.get("preferred_username", email)
    locale = raw_claims.get("locale", "")
    zoneinfo = raw_claims.get("zoneinfo", "")

    # Extract Okta-specific custom claims if present
    custom_claims = {
        k: v for k, v in raw_claims.items()
        if k.startswith("custom_") or k not in (
            "sub", "email", "email_verified", "given_name", "family_name",
            "name", "preferred_username", "locale", "zoneinfo",
            "iss", "aud", "iat", "exp", "auth_time", "nonce",
        )
    }

    return FederatedUserClaims(
        provider="okta",
        provider_user_id=sub,
        email=email,
        email_verified=bool(email_verified),
        given_name=given_name,
        family_name=family_name,
        full_name=full_name,
        preferred_username=preferred_username,
        locale=locale,
        timezone=zoneinfo,
        raw_claims=raw_claims,
        custom_attributes=custom_claims,
        fetched_at=int(time.time()),
    )


def fetch_and_normalize_profile(access_token: str) -> ClaimNormalizationResult:
    """
    Fetch Okta userinfo and normalize claims into internal format.

    Returns ClaimNormalizationResult with status, claims, and any errors.
    """
    try:
        raw_claims = fetch_userinfo(access_token)
        normalized = normalize_okta_claims(raw_claims)

        return ClaimNormalizationResult(
            success=True,
            claims=normalized,
            provider="okta",
            fetched_at=normalized.fetched_at,
        )
    except OktaUserinfoError as e:
        return ClaimNormalizationResult(
            success=False,
            error=str(e),
            provider="okta",
            fetched_at=int(time.time()),
        )
    except Exception as e:
        return ClaimNormalizationResult(
            success=False,
            error=f"Unexpected error: {str(e)}",
            provider="okta",
            fetched_at=int(time.time()),
        )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        token = sys.argv[1]
        result = fetch_and_normalize_profile(token)
        print(result.model_dump_json(indent=2) if hasattr(result, "model_dump_json") else result)
