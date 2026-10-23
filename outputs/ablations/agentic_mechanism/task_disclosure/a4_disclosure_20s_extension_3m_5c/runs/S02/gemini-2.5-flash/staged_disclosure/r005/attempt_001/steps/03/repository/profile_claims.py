
import json

def fetch_and_normalize_google_profile_claims(access_token: str):
    """
    Fetches user profile claims from Google's UserInfo API and normalizes them.

    Args:
        access_token: A valid OAuth2 access token for the Google API.

    Returns:
        A dictionary of normalized user profile claims.
    """
    google_userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    # In a real application, you would make an HTTP request here:
    # import requests
    # headers = {"Authorization": f"Bearer {access_token}"}
    # response = requests.get(google_userinfo_url, headers=headers)
    # response.raise_for_status()
    # claims = response.json()

    # For demonstration, we'll use mock claims.
    # Replace this with actual API call in a real implementation.
    mock_claims = {
        "sub": "1234567890",
        "name": "John Doe",
        "given_name": "John",
        "family_name": "Doe",
        "picture": "https://example.com/john.jpg",
        "email": "john.doe@example.com",
        "email_verified": True,
        "locale": "en",
    }
    claims = mock_claims

    normalized_claims = {
        "id": claims.get("sub"),
        "first_name": claims.get("given_name"),
        "last_name": claims.get("family_name"),
        "full_name": claims.get("name"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "profile_picture": claims.get("picture"),
        "locale": claims.get("locale"),
        "provider": "google" # Identifies the provider
    }
    return normalized_claims

if __name__ == "__main__":
    # Example usage (replace with a real access token in a live environment)
    # For testing, you can call the function with a dummy access token.
    # In a real scenario, you would obtain an access token via OAuth2 flow.
    dummy_access_token = "YOUR_GOOGLE_ACCESS_TOKEN"
    profile_data = fetch_and_normalize_google_profile_claims(dummy_access_token)
    print(json.dumps(profile_data, indent=2))
