# profile_claims.py
# [SAME-SCENARIO] Fetches and normalizes federated user profile claims

import json
from typing import Dict, Any

from identity_client import FederatedIdpClient, UserNotFoundError


def fetch_and_normalize_claims(user_id: str, provider: str) -> Dict[str, Any]:
    """Retrieve user profile information from the identity provider and normalize.

    Args:
        user_id (str): Identifier of the federated user (subject/unique ID).
        provider (str): Identity provider identifier (e.g., 'google', 'okta').

    Returns:
        Dict[str, Any]: Normalized claim set with consistent field names.
    """
    config = FederatedIdpClient.from_env(provider)
    try:
        # Provider-specific method to fetch profile data; returns raw JSON
        raw_profile = config.get_user_profile(user_id)
    except UserNotFoundError as exc:
        raise UserNotFoundError(f"User {user_id} not found at {provider}: {exc}")

    # Normalization logic: map provider-specific fields to a common schema
    normalized = {
        "user_id": raw_profile.get("sub") or user_id,
        "email": raw_profile.get("email") or raw_profile.get("mail"),
        "full_name": raw_profile.get("name") or raw_profile.get("displayName"),
        "given_name": raw_profile.get("given_name") or raw_profile.get("firstName"),
        "family_name": raw_profile.get("family_name") or raw_profile.get("lastName"),
        "picture_url": raw_profile.get("picture") or raw_profile.get("avatar"),
        "locale": raw_profile.get("locale") or raw_profile.get("preferredLanguage"),
        # Add any extra fields as needed
    }
    # Ensure no None values are stored
    normalized = {k: v for k, v in normalized.items() if v is not None}
    return normalized


if __name__ == "__main__":
    # Example usage (replace with real user ID and provider in production)
    user_id = "123456789"
    provider = "google"
    try:
        claims = fetch_and_normalize_claims(user_id, provider)
        print("Normalized claims:", json.dumps(claims, indent=2))
    except UserNotFoundError as e:
        print(e)
