import os
import requests
import json
from typing import Dict, Any


def fetch_and_normalize_auth0_profile(access_token: str) -> Dict[str, Any]:
    """
    Fetches user profile claims from Auth0's /userinfo endpoint and normalizes them.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        profile = response.json()

        # Normalize claims (example: mapping Auth0-specific claims to a generic structure)
        normalized_profile = {
            "sub": profile.get("sub"),
            "name": profile.get("name"),
            "email": profile.get("email"),
            "email_verified": profile.get("email_verified"),
            "picture": profile.get("picture"),
            "locale": profile.get("locale"),
            "updated_at": profile.get("updated_at"),
            # Add other claims as needed
        }
        return normalized_profile
    except requests.exceptions.RequestException as e:
        print(f"Error fetching or normalizing profile: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # This is an example. In a real application, the access_token would come from the OAuth callback.
    example_access_token = "YOUR_ACCESS_TOKEN_HERE"
    if example_access_token == "YOUR_ACCESS_TOKEN_HERE":
        print("Please replace 'YOUR_ACCESS_TOKEN_HERE' with an actual access token.")
    else:
        profile_claims = fetch_and_normalize_auth0_profile(example_access_token)
        print(json.dumps(profile_claims, indent=2))
