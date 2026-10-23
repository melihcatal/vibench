import os
import requests
from identity_models import UserProfile

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")


def fetch_and_normalize_profile_claims(access_token: str) -> UserProfile:
    """Fetches user profile claims from Auth0's /userinfo endpoint and normalizes them."""
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    # Normalize claims into a consistent UserProfile model
    user_profile = UserProfile(
        sub=claims.get("sub"),
        name=claims.get("name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified", False),
        picture=claims.get("picture"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
    )
    return user_profile


if __name__ == "__main__":
    # Placeholder for demonstration
    sample_access_token = "YOUR_AUTH0_ACCESS_TOKEN_HERE"
    try:
        profile = fetch_and_normalize_profile_claims(sample_access_token)
        print("Normalized User Profile:")
        print(profile.model_dump_json(indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching profile claims: {e}")
