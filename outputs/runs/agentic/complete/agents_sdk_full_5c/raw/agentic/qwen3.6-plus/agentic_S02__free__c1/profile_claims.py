"""
Fetch and normalize federated user profile claims from Auth0.

After token exchange, this module retrieves the user's profile information
from the Auth0 /userinfo endpoint and the ID token, then normalizes the
claims into a consistent UserProfileClaims structure regardless of the
identity provider (Google, GitHub, Okta, etc.) used within Auth0.
"""

import os
from typing import Any, Dict, List, Optional

from identity_models import (
    UserProfileClaims,
    normalize_claims,
    extract_id_token_claims,
)
from identity_client import IdentityClient


# Auth0-specific custom claim namespace
AUTH0_NAMESPACE = os.environ.get(
    "AUTH0_CLAIM_NAMESPACE",
    "https://dev-example.us.auth0.com",
)


def fetch_user_profile(
    access_token: str,
    client: Optional[IdentityClient] = None,
) -> Dict[str, Any]:
    """
    Fetch the user profile from the Auth0 /userinfo endpoint.

    Auth0 returns OIDC standard claims plus any custom claims added
    via Auth0 Rules or Actions. The response format depends on the
    scopes requested during authorization.
    """
    if client is None:
        client = IdentityClient()

    userinfo = client.get_user_info(access_token)
    return userinfo


def fetch_and_merge_claims(
    access_token: str,
    id_token: Optional[str] = None,
    client: Optional[IdentityClient] = None,
) -> Dict[str, Any]:
    """
    Fetch claims from Auth0 /userinfo and merge with ID token claims.

    Auth0 may return slightly different claim sets from the userinfo
    endpoint versus the ID token. This function merges both sources,
    preferring userinfo claims for overlapping keys since userinfo
    is the most authoritative source per the OIDC specification.
    """
    userinfo = fetch_user_profile(access_token, client)

    merged: Dict[str, Any] = dict(userinfo)

    if id_token:
        id_claims = extract_id_token_claims(id_token)
        for key, value in id_claims.items():
            if key not in merged:
                merged[key] = value

    return merged


def normalize_auth0_profile(
    access_token: str,
    id_token: Optional[str] = None,
    client: Optional[IdentityClient] = None,
) -> UserProfileClaims:
    """
    Fetch, merge, and normalize a federated user profile from Auth0.

    Retrieves claims from Auth0's /userinfo endpoint, merges with the
    ID token, and normalizes them into a UserProfileClaims object.
    Auth0-specific custom claims under the configured namespace are
    extracted into the custom_claims field.

    Auth0 provides provider-specific attributes:
    - For Google: email_verified, picture, hd (hosted domain)
    - For GitHub: name, picture (avatar_url), nickname
    - For enterprise SAML/OIDC: roles, groups, departments
    """
    merged_claims = fetch_and_merge_claims(access_token, id_token, client)

    idp_name = merged_claims.get("iss", "auth0")
    profile = normalize_claims(merged_claims, provider="auth0")

    profile.idp_name = idp_name

    if not profile.name and profile.given_name and profile.family_name:
        profile.name = f"{profile.given_name} {profile.family_name}"

    custom_ns = AUTH0_NAMESPACE.rstrip("/")
    for key, value in merged_claims.items():
        if key.startswith(custom_ns):
            short_key = key[len(custom_ns) + 1:]
            profile.custom_claims[short_key] = value

    auth0_specific = merged_claims.get("identities", [])
    if auth0_specific:
        profile.custom_claims["auth0_identities"] = auth0_specific

    last_login = merged_claims.get("updated_at")
    if last_login:
        profile.custom_claims["last_login"] = last_login

    created_at = merged_claims.get("created_at")
    if created_at:
        profile.custom_claims["created_at"] = created_at

    return profile


def get_auth0_user_roles(
    access_token: str,
    client: Optional[IdentityClient] = None,
) -> List[str]:
    """
    Extract user roles from Auth0 profile claims.

    Auth0 stores roles in custom claims (typically under a namespace)
    or via the Management API. This function checks both the ID token
    claims and the userinfo response for role information.
    """
    merged = fetch_and_merge_claims(access_token, client=client)

    roles: List[str] = []

    for key in ("roles", "https://example.com/roles", f"{AUTH0_NAMESPACE}/roles"):
        if key in merged:
            val = merged[key]
            if isinstance(val, list):
                roles.extend(val)
            elif isinstance(val, str):
                roles.append(val)

    auth0_identities = merged.get("identities", [])
    for identity in auth0_identities:
        if isinstance(identity, dict):
            id_roles = identity.get("roles", [])
            if isinstance(id_roles, list):
                roles.extend(id_roles)

    return list(set(roles))


def get_auth0_user_metadata(
    access_token: str,
    client: Optional[IdentityClient] = None,
) -> Dict[str, Any]:
    """
    Extract Auth0 user_metadata and app_metadata from profile claims.

    Auth0 allows storing custom user data in user_metadata (editable
    by the user) and app_metadata (set by the application). These are
    available via the /userinfo endpoint when included in the scopes
    or via Auth0 Actions.
    """
    merged = fetch_and_merge_claims(access_token, client=client)

    metadata: Dict[str, Any] = {}

    for key in merged:
        if "user_metadata" in key or "app_metadata" in key:
            metadata[key] = merged[key]

    custom_ns = AUTH0_NAMESPACE.rstrip("/")
    for key, value in merged.items():
        if key.startswith(custom_ns):
            short_key = key[len(custom_ns) + 1:]
            if "metadata" in short_key:
                metadata[short_key] = value

    return metadata


def extract_provider_specific_claims(
    claims: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extract provider-specific claims from an Auth0 federated profile.

    Auth0 normalizes claims from upstream providers (Google, GitHub,
    Okta, Azure AD, etc.) but also preserves provider-specific
    attributes. This function identifies and extracts them.
    """
    provider_claims: Dict[str, Any] = {}

    google_specific = {
        "hd", "locale", "email_verified",
    }
    github_specific = {
        "nickname", "blog", "company", "location",
    }
    azure_ad_specific = {
        "oid", "tid", "ipaddr", "acct",
    }

    identities = claims.get("identities", [])
    if identities and isinstance(identities, list) and len(identities) > 0:
        provider = identities[0].get("provider", "")
        provider_claims["upstream_provider"] = provider

    for key, value in claims.items():
        if key in google_specific:
            provider_claims[f"google:{key}"] = value
        elif key in github_specific:
            provider_claims[f"github:{key}"] = value
        elif key in azure_ad_specific:
            provider_claims[f"azure_ad:{key}"] = value

    return provider_claims


if __name__ == "__main__":
    print("Auth0 profile claims handler ready.")
    print(f"Claim namespace: {AUTH0_NAMESPACE}")
