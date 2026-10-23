import os
import requests
from typing import Dict, Any

def fetch_auth0_profile_claims(access_token: str) -> Dict[str, Any]:
    """
    Fetches and normalizes user profile claims from Auth0's Userinfo endpoint.
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    userinfo_url = f"https://{auth0_domain}/userinfo"

    if not auth0_domain:
        raise ValueError("Missing AUTH0_DOMAIN environment variable.")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    # Normalize claims (example: ensuring 'sub' and 'email' are present)
    normalized_claims = {
        "sub": claims.get("sub"),
        "email": claims.get("email"),
        "name": claims.get("name"),
        "picture": claims.get("picture"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
    }
    return normalized_claims

if __name__ == "__main__":
    # Example usage (replace with an actual Auth0 access token)
    example_access_token = "your_auth0_access_token_here"
    os.environ["AUTH0_DOMAIN"] = "dev-your-tenant.us.auth0.com" # Replace with your Auth0 domain
    try:
        profile = fetch_auth0_profile_claims(example_access_token)
        print("Fetched and normalized profile claims:")
        print(profile)
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching profile claims: {e.response.text}")
    except ValueError as e:
        print(f"Configuration error: {e}")
