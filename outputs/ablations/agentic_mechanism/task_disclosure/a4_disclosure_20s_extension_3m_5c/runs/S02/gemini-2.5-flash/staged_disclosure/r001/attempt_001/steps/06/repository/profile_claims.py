
def get_and_normalize_auth0_claims(user_profile: dict) -> dict:
    """
    Fetches and normalizes federated user profile claims from an Auth0-like structure.
    """
    auth0_claims = user_profile

    normalized_claims = {
        "sub": auth0_claims.get("sub"),
        "name": auth0_claims.get("name"),
        "email": auth0_claims.get("email"),
        "email_verified": auth0_claims.get("email_verified", False),
        "picture": auth0_claims.get("picture"),
        "updated_at": auth0_claims.get("updated_at"),
        "locale": auth0_claims.get("locale"),
        # Add other claims as needed and normalize their names
        "auth0_user_id": auth0_claims.get("user_id"), # Provider-specific identifier
        "auth0_nickname": auth0_claims.get("nickname")
    }
    return normalized_claims

