import os
import requests
import json

def fetch_auth0_user_profile(access_token: str) -> dict:
    """
    Fetches user profile claims from Auth0's /userinfo endpoint.

    Args:
        access_token: The access token obtained after the authorization flow.

    Returns:
        A dictionary containing the normalized user profile claims.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

    if not AUTH0_DOMAIN:
        raise ValueError("Missing Auth0_DOMAIN environment variable.")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors

    claims = response.json()

    # Normalize claims to a common structure
    normalized_claims = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified", False),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
        "updated_at": claims.get("updated_at"),
        # Add other claims as needed
        "original_claims": claims # Keep original claims for debugging/completeness
    }
    return normalized_claims

if __name__ == "__main__":
    # Example usage (not part of the core logic)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"

    # This dummy token will not work with a real Auth0 endpoint
    dummy_access_token = "eyJ..." 
    try:
        # This call will likely fail without a valid token and actual Auth0 setup
        user_profile = fetch_auth0_user_profile(dummy_access_token)
        print(f"Fetched and normalized user profile: {user_profile}")
    except Exception as e:
        print(f"Error fetching user profile: {e}")
