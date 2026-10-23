import requests
import json

from identity_client import AUTH0_DOMAIN
from identity_models import UserProfileClaims

def fetch_and_normalize_profile_claims(access_token: str) -> UserProfileClaims:
    """
    Fetches user profile claims from Auth0's /userinfo endpoint and normalizes them.
    """
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        raw_claims = response.json()

        # Normalize claims to a common structure
        normalized_claims = UserProfileClaims(
            sub=raw_claims.get("sub"),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            email=raw_claims.get("email"),
            email_verified=raw_claims.get("email_verified"),
            picture=raw_claims.get("picture"),
            locale=raw_claims.get("locale"),
            updated_at=raw_claims.get("updated_at"),
            raw_claims=raw_claims # Store the raw claims for completeness
        )
        return normalized_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user profile claims: {e}")
        raise

if __name__ == "__main__":
    # This is a simplified example. In a real application, 'access_token'
    # would come from a successful OAuth token exchange.
    print("This script demonstrates fetching and normalizing user profile claims.")
    # Example usage (replace with actual access token)
    # try:
    #     dummy_access_token = "YOUR_ACCESS_TOKEN_HERE"
    #     profile = fetch_and_normalize_profile_claims(dummy_access_token)
    #     print("Successfully fetched and normalized profile claims:")
    #     print(json.dumps(profile.to_dict(), indent=2))
    # except Exception as e:
    #     print(f"Failed to get profile claims: {e}")
