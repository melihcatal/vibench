import os
import requests
import json

class Auth0ProfileClaims:
    def __init__(self, domain: str):
        self.domain = domain

    def fetch_user_profile(self, access_token: str) -> dict:
        """Fetches user profile claims from Auth0's /userinfo endpoint."""
        userinfo_url = f"https://{self.domain}/userinfo"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()

    def normalize_claims(self, claims: dict) -> dict:
        """Normalizes a subset of common claims."""
        normalized = {
            "sub": claims.get("sub"),
            "name": claims.get("name"),
            "email": claims.get("email"),
            "email_verified": claims.get("email_verified"),
            "picture": claims.get("picture"),
            "updated_at": claims.get("updated_at"),
        }
        return {k: v for k, v in normalized.items() if v is not None}

if __name__ == "__main__":
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN")

    # In a real application, the access_token would come from the oauth_callback step
    # For demonstration purposes, use a placeholder.
    example_access_token = "dummy_access_token_from_auth0"

    profile_fetcher = Auth0ProfileClaims(AUTH0_DOMAIN)
    try:
        user_claims = profile_fetcher.fetch_user_profile(example_access_token)
        print("Raw User Claims:")
        print(json.dumps(user_claims, indent=2))

        normalized_claims = profile_fetcher.normalize_claims(user_claims)
        print("\nNormalized User Claims:")
        print(json.dumps(normalized_claims, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching user profile: {e}")
        if e.response is not None:
            print(e.response.json())
