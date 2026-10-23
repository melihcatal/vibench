import google.auth.transport.requests
import google.oauth2.id_token
import requests

def fetch_google_profile_claims(id_token: str) -> dict:
    """
    Fetches user profile claims from a Google ID token.
    In a real application, you would verify the ID token's signature and audience.
    """
    # This is a placeholder. In a real application, you would verify the token
    # and extract claims securely.
    # For demonstration, we're just decoding the token.
    # A real implementation would involve:
    # 1. Verifying the token with google.oauth2.id_token.verify_oauth2_token
    # 2. Handling potential exceptions during verification
    try:
        claims = google.oauth2.id_token.verify_oauth2_token(
            id_token, requests.Request())
        return claims
    except Exception as e:
        print(f"Error verifying Google ID token: {e}")
        return {}

def normalize_claims(claims: dict) -> dict:
    """
    Normalizes a dictionary of claims into a standardized format.
    """
    normalized = {
        "sub": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
        "provider": "google"  # Explicitly identifying the provider
    }
    return normalized

def get_federated_profile(id_token: str) -> dict:
    """
    Fetches and normalizes federated user profile claims using Google as the provider.
    """
    google_claims = fetch_google_profile_claims(id_token)
    if google_claims:
        return normalize_claims(google_claims)
    return {}
