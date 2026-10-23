import identity_models

# Concrete provider: Auth0 (OIDC compliant)
def extract_profile_claims(id_token):
    """Parse Auth0-issued JWT and normalise claims."""
    # In production, verify signature with Auth0's public key before usage.
    json_claims = identity_models.decode_jwt(id_token)
    # Map Auth0 fields to generic federated schema
    normalized = {
        "sub": json_claims.get("sub"),
        "name": json_claims.get("name"),
        "email": json_claims.get("email"),
        "email_verified": json_claims.get("email_verified"),
        "locale": json_claims.get("locale"),
        "picture": json_claims.get("picture"),
    }
    return normalized

if __name__ == "__main__":
    # Example usage (requires real id_token and decode_jwt implementation)
    pass
