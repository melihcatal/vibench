import os
import json

# Helper utilities for Federated Login Flow
# Provide a central place for configuration loading and small payload utilities


def load_config(key, default=None):
    """Read configuration value from environment with optional fallback.
    Args:
        key (str): Environment variable name.
        default (any, optional): Value to return if env var is missing.
    Returns:
        any: Config value or default.
    """
    return os.getenv(key, default)


def normalize_claims(raw_claims):
    """Map provider-specific claim dicts to a consistent internal shape.
    Args:
        raw_claims (dict): Raw claims from Cognito, Auth0, etc.
    Returns:
        dict: Normalized claims using standard OIDC keys.
    """
    # Example: convert nested attributes into flat keys whenever possible
    normalized = {
        "sub": raw_claims.get("sub") or raw_claims.get("user_id"),
        "email": raw_claims.get("email"),
        "email_verified": raw_claims.get("email_verified"),
        "name": raw_claims.get("name"),
        "given_name": raw_claims.get("given_name"),
        "family_name": raw_claims.get("family_name"),
        # Add more mappings as needed
    }
    return normalized


# Example usage in any same-scenario file
# cfg = load_config('COGNITO_CLIENT_ID')
# profile = normalize_claims(cognito_response)
