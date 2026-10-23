import os
import requests
from typing import Optional, Dict, Any
from identity_client import IdentityClient
from identity_models import UserProfileClaims


def fetch_and_normalize_profile_claims(
    access_token: str,
) -> Optional[UserProfileClaims]:
    """Fetches and normalizes federated user profile claims using Auth0 /userinfo endpoint."""
    client = IdentityClient()
    userinfo_url = client.get_userinfo_url()

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        raw_claims = response.json()

        # Normalize claims to a common structure
        normalized_claims = UserProfileClaims(
            sub=raw_claims.get("sub"),
            email=raw_claims.get("email"),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture=raw_claims.get("picture"),
            locale=raw_claims.get("locale"),
            raw_claims=raw_claims,  # Keep raw claims for completeness
        )
        return normalized_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info: {e}")
        print(f"Response content: {response.text if response else 'No response'}")
        return None


if __name__ == "__main__":
    # Example usage (in a real application, access_token would come from a successful login)
    # Set environment variables for AUTH0_DOMAIN
    # os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN"
    #
    # A dummy access token for demonstration
    # dummy_access_token = "some_valid_access_token_from_auth0"
    #
    # claims = fetch_and_normalize_profile_claims(dummy_access_token)
    # if claims:
    #     print(f"User Subject: {claims.sub}")
    #     print(f"User Email: {claims.email}")
    # else:
    #     print("Failed to fetch or normalize profile claims.")
    pass  # placeholder to avoid runtime error if __name__ is run without actual env vars
