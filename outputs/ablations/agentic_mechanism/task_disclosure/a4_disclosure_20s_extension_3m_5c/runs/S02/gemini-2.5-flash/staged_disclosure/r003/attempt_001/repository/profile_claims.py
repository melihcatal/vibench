
# profile_claims.py

AUTH0_DOMAIN = "YOUR_AUTH0_DOMAIN.auth0.com" # Provider-specific identifier

def fetch_claims_from_auth0(user_id: str) -> dict:
    """
    Simulates fetching federated user profile claims from Auth0.
    In a real application, this would involve using the Auth0 Management API or
    retrieving claims from an authenticated token.
    """
    print(f"Fetching claims for user {user_id} from {AUTH0_DOMAIN}...")
    # This is a mock response. In a real scenario, you'd make an API call.
    if user_id == "user123":
        return {
            "sub": "auth0|user123",
            "nickname": "testuser",
            "name": "Test User",
            "picture": "https://example.com/pic.png",
            "updated_at": "2023-01-01T12:00:00.000Z",
            "email": "testuser@example.com",
            "email_verified": True,
            "custom_data": {"level": 10, "theme": "dark"}
        }
    return {}

def normalize_claims(claims: dict) -> dict:
    """
    Normalizes the fetched claims into a consistent format.
    """
    normalized = {
        "user_id": claims.get("sub"),
        "username": claims.get("nickname"),
        "full_name": claims.get("name"),
        "profile_picture": claims.get("picture"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified", False),
        "last_updated": claims.get("updated_at"),
        # You can map custom claims or additional fields as needed
        "metadata": claims.get("custom_data", {})
    }
    return normalized

if __name__ == "__main__":
    user_id_to_fetch = "user123"
    raw_claims = fetch_claims_from_auth0(user_id_to_fetch)

    if raw_claims:
        normalized_user_profile = normalize_claims(raw_claims)
        print("\nRaw Claims:")
        for key, value in raw_claims.items():
            print(f"  {key}: {value}")
        print("\nNormalized Profile:")
        for key, value in normalized_user_profile.items():
            print(f"  {key}: {value}")
    else:
        print(f"No claims found for user {user_id_to_fetch}")
