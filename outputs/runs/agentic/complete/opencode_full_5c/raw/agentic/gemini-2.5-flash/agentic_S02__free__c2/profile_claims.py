import os
import requests
from typing import Dict, Any
from identity_client import Auth0Config
from identity_models import UserProfile


def fetch_and_normalize_profile_claims(access_token: str) -> UserProfile:
    # Auth0 USERINFO_URL is an identifiable signal
    userinfo_url = Auth0Config.USERINFO_URL

    headers = {"Authorization": f"Bearer {{access_token}}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()

    claims: Dict[str, Any] = response.json()
    print("Fetched raw claims:")
    print(claims)

    # Normalize claims into our UserProfile model
    normalized_profile = UserProfile(
        sub=claims.get("sub", ""),
        name=claims.get("name"),
        email=claims.get("email"),
        picture=claims.get("picture"),
        raw_claims=claims,
    )
    print("Normalized profile:")
    print(normalized_profile)
    return normalized_profile


if __name__ == "__main__":
    # Example usage (replace with actual access token)
    dummy_access_token = "your_auth0_access_token"
    if dummy_access_token == "your_auth0_access_token":
        print(
            "Please replace 'your_auth0_access_token' with a real access token to test."
        )
    else:
        try:
            fetch_and_normalize_profile_claims(dummy_access_token)
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching profile claims: {e.response.text}")
