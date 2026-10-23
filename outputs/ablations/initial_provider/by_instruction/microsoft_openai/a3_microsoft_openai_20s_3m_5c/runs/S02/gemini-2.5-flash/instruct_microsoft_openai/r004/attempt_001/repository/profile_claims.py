import os
import requests
import json

# Google Identity Platform Configuration
# This assumes an access token has already been obtained, e.g., from an OAuth flow.

def fetch_google_userinfo(access_token: str):
    """
    Fetches user profile claims from Google's UserInfo endpoint.
    Requires an access token with appropriate scopes (e.g., openid, email, profile).
    """
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        user_claims = response.json()
        return user_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google user info: {e}")
        return None

def normalize_google_claims(raw_claims: dict):
    """
    Normalizes raw claims from Google UserInfo into a common format.
    """
    normalized_claims = {
        "sub": raw_claims.get("sub"),
        "name": raw_claims.get("name"),
        "given_name": raw_claims.get("given_name"),
        "family_name": raw_claims.get("family_name"),
        "email": raw_claims.get("email"),
        "email_verified": raw_claims.get("email_verified", False),
        "picture": raw_claims.get("picture"),
        "locale": raw_claims.get("locale"),
        "provider": "google" # Custom field to identify the provider
    }
    return normalized_claims

if __name__ == "__main__":
    # Example usage (replace with a real access token)
    # For a real run, an access_token would be dynamically obtained.
    sample_access_token = "YOUR_GOOGLE_ACCESS_TOKEN_HERE"

    # raw_claims = fetch_google_userinfo(sample_access_token)
    # if raw_claims:
    #     print("Raw Google Claims:")
    #     print(json.dumps(raw_claims, indent=2))
    #     normalized = normalize_google_claims(raw_claims)
    #     print("\nNormalized Claims:")
    #     print(json.dumps(normalized, indent=2))
    # else:
    #     print("Failed to fetch Google user info.")
    print("To test, provide a Google access token to fetch_google_userinfo.")
