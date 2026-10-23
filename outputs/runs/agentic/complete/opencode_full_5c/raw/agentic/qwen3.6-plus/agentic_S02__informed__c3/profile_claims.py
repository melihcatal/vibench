import os
import json
import time
from typing import Dict, Any, Optional, List

from identity_models import OAuthConfig, UserProfile
from identity_client import (
    get_oauth_config,
    fetch_user_profile,
    generate_event_id,
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
)


def fetch_and_normalize_profile(
    access_token: str,
    config: Optional[OAuthConfig] = None,
) -> Dict[str, Any]:
    if config is None:
        config = get_oauth_config()

    profile = fetch_user_profile(access_token, config)

    audit_event = {
        "event_id": generate_event_id(),
        "event_type": "profile_fetch",
        "timestamp": time.time(),
        "user_sub": profile.sub,
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "success": True,
    }

    return {
        "success": True,
        "profile": profile.to_dict(),
        "audit_event": audit_event,
        "provider": "auth0",
    }


def extract_standard_claims(raw_claims: Dict[str, Any]) -> Dict[str, Any]:
    standard_claims = {
        "sub": raw_claims.get("sub", ""),
        "name": raw_claims.get("name", ""),
        "given_name": raw_claims.get("given_name", ""),
        "family_name": raw_claims.get("family_name", ""),
        "middle_name": raw_claims.get("middle_name", ""),
        "nickname": raw_claims.get(
            "nickname", raw_claims.get("preferred_username", "")
        ),
        "email": raw_claims.get("email", ""),
        "email_verified": raw_claims.get("email_verified", False),
        "picture": raw_claims.get("picture", ""),
        "locale": raw_claims.get("locale", ""),
        "updated_at": raw_claims.get("updated_at", ""),
    }
    return standard_claims


def extract_auth0_specific_claims(raw_claims: Dict[str, Any]) -> Dict[str, Any]:
    auth0_claims = {
        "auth0_user_id": raw_claims.get("sub", ""),
        "auth0_connection": raw_claims.get("identities", [{}])[0].get("connection", "")
        if raw_claims.get("identities")
        else "",
        "auth0_provider": raw_claims.get("identities", [{}])[0].get("provider", "")
        if raw_claims.get("identities")
        else "",
        "auth0_created_at": raw_claims.get("created_at", ""),
        "auth0_updated_at": raw_claims.get("updated_at", ""),
        "auth0_email_verified": raw_claims.get("email_verified", False),
        "auth0_phone_number": raw_claims.get("phone_number", ""),
        "auth0_phone_verified": raw_claims.get("phone_verified", False),
    }
    return auth0_claims


def normalize_roles_and_permissions(raw_claims: Dict[str, Any]) -> Dict[str, List[str]]:
    roles = raw_claims.get("https://example.com/roles", [])
    permissions = raw_claims.get("https://example.com/permissions", [])

    if isinstance(roles, str):
        roles = [roles]
    if isinstance(permissions, str):
        permissions = [permissions]

    return {
        "roles": list(roles) if roles else [],
        "permissions": list(permissions) if permissions else [],
    }


def get_enriched_profile(
    access_token: str,
    config: Optional[OAuthConfig] = None,
) -> Dict[str, Any]:
    if config is None:
        config = get_oauth_config()

    profile = fetch_user_profile(access_token, config)

    standard_claims = extract_standard_claims(profile.raw_claims)
    auth0_claims = extract_auth0_specific_claims(profile.raw_claims)
    roles_perms = normalize_roles_and_permissions(profile.raw_claims)

    enriched = {
        "standard_claims": standard_claims,
        "auth0_claims": auth0_claims,
        "roles_and_permissions": roles_perms,
        "raw_claims": profile.raw_claims,
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
    }

    return enriched


if __name__ == "__main__":
    sample_claims = {
        "sub": "auth0|12345",
        "name": "Test User",
        "email": "test@example.com",
        "email_verified": True,
        "picture": "https://example.com/avatar.png",
        "nickname": "testuser",
        "identities": [{"connection": "google-oauth2", "provider": "google"}],
        "created_at": "2024-01-01T00:00:00.000Z",
    }
    result = extract_standard_claims(sample_claims)
    print(json.dumps(result, indent=2))
