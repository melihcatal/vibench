import os
import requests
from identity_client import Auth0Config
from identity_models import UserProfile
from typing import Dict, Any


def fetch_and_normalize_auth0_profile(access_token: str) -> UserProfile:
    """
    Fetches user profile claims from Auth0's /userinfo endpoint
    and normalizes them into a UserProfile object.
    """
    if not Auth0Config.DOMAIN:
        raise ValueError("Auth0_DOMAIN environment variable is not set.")

    userinfo_url = f"https://{Auth0Config.DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    user_claims: Dict[str, Any] = response.json()

    # Basic normalization
    normalized_profile = UserProfile(
        sub=user_claims.get("sub"),
        email=user_claims.get("email"),
        name=user_claims.get("name"),
        picture=user_claims.get("picture"),
        normalized_claims=user_claims,  # Store all claims as-is for now
    )
    return normalized_profile


if __name__ == "__main__":
    # Example usage: Replace 'your_access_token' with a real access token
    # obtained from the OAuth callback.
    example_access_token = "YOUR_AUTH0_ACCESS_TOKEN"
    if example_access_token == "YOUR_AUTH0_ACCESS_TOKEN":
        print(
            "Please replace 'YOUR_AUTH0_ACCESS_TOKEN' with an actual access token for testing."
        )
    else:
        try:
            profile = fetch_and_normalize_auth0_profile(example_access_token)
            print("Fetched and Normalized User Profile:")
            print(f"Subject: {profile.sub}")
            print(f"Email: {profile.email}")
            print(f"Name: {profile.name}")
            print(f"Picture: {profile.picture}")
            print(f"All Claims: {profile.normalized_claims}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile: {e}")
        except ValueError as e:
            print(f"Configuration error: {e}")
