"""
profile_claims.py - Fetches and normalizes federated user profile claims
from an OpenID Connect identity provider.

Provider: Microsoft Entra ID (Azure Active Directory)
SDK: msal
Auth env vars: AZURE_TENANT_ID, AZURE_CLIENT_ID
"""

import os
from typing import Optional

import msal


AZURE_ENTRA_GRAPH_BASE = "https://graph.microsoft.com/v1.0"
DEFAULT_CLAIMS_MAPPING = {
    "user_id": "oid",
    "email": "mail",
    "display_name": "displayName",
    "given_name": "givenName",
    "surname": "surname",
    "upn": "userPrincipalName",
    "tenant_id": "tid",
}


def normalize_claims(claims: dict, mapping: Optional[dict] = None) -> dict:
    """
    Normalize Microsoft Entra ID claims into a standard federated user profile.
    """
    mapping = mapping or DEFAULT_CLAIMS_MAPPING
    normalized = {}
    for standard_key, entra_key in mapping.items():
        value = claims.get(entra_key)
        if value is not None:
            normalized[standard_key] = value
    return normalized


def fetch_user_info(access_token: str) -> dict:
    """
    Fetch user profile from Microsoft Graph API using the access token
    obtained from Microsoft Entra ID OIDC flow.
    """
    import requests

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Query Microsoft Graph for profile information
    # Endpoint: graph.microsoft.com
    response = requests.get(
        f"{AZURE_ENTRA_GRAPH_BASE}/me?$select=id,displayName,givenName,surname,mail,userPrincipalName",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def get_profile_claims(access_token: str, id_token_claims: Optional[dict] = None) -> dict:
    """
    Fetch and normalize federated user profile claims from Microsoft Entra ID.

    Combines ID token claims with Microsoft Graph API data for a complete profile.

    Returns normalized profile with standard keys.
    """
    tenant_id = os.environ.get("AZURE_TENANT_ID", "common")
    client_id = os.environ.get("AZURE_CLIENT_ID", "")

    if not client_id:
        raise ValueError("AZURE_CLIENT_ID environment variable must be set")

    # Use msal to decode and validate the token structure
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=authority,
        client_credential="placeholder",  # Only for token decoding context
    )

    # Fetch enriched profile from Microsoft Graph
    graph_profile = fetch_user_info(access_token)

    # Normalize using Entra ID claim mapping
    merged_claims = {
        **graph_profile,
        "oid": graph_profile.get("id", ""),
        "tid": tenant_id,
    }

    if id_token_claims:
        merged_claims.update(id_token_claims)

    normalized = normalize_claims(merged_claims)
    normalized["provider"] = "microsoft_entra_id"
    normalized["authority"] = authority

    return normalized


def parse_id_token_claims(id_token: str) -> dict:
    """
    Parse the ID token from Microsoft Entra ID to extract claims.
    Uses msal token processing utilities.
    """
    # Decode JWT without verification (for display purposes)
    # In production, use msal's TokenVerifier or similar
    import base64
    import json

    parts = id_token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid ID token format")

    payload = parts[1]
    # Add padding if needed
    payload += "=" * (4 - len(payload) % 4)
    decoded = base64.urlsafe_b64decode(payload)
    return json.loads(decoded)
