import requests
from typing import Dict, Any
from identity_client import Auth0Client
from identity_models import UserProfile


def fetch_and_normalize_profile_claims(access_token: str) -> UserProfile:
    """Fetches and normalizes federated user profile claims using Auth0's /userinfo endpoint."""
    client = Auth0Client()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(client.get_userinfo_url(), headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    claims: Dict[str, Any] = response.json()

    # Normalize claims to a common UserProfile structure
    return UserProfile(
        sub=claims.get("sub", ""),
        name=claims.get("name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        picture=claims.get("picture"),
        raw_claims=claims,
    )


# Example usage (not part of the file, just for demonstration):
# if __name__ == "__main__":
#     import os
#     os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
#     os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
#     os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"
#     # This access token would come from the oauth_callback.py step
#     sample_access_token = "YOUR_USERS_ACCESS_TOKEN"
#     try:
#         user_profile = fetch_and_normalize_profile_claims(sample_access_token)
#         print(f"User Subject: {user_profile.sub}")
#         print(f"User Email: {user_profile.email}")
#         print(f"Raw Claims: {user_profile.raw_claims}")
#     except requests.exceptions.HTTPError as e:
#         print(f"Error fetching profile: {e.response.text}")
#     except ValueError as e:
#         print(f"Configuration Error: {e}")
