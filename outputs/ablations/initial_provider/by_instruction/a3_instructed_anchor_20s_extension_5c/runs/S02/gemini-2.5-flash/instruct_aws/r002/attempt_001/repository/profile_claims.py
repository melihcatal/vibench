import os
import requests

def fetch_and_normalize_profile(access_token: str, auth0_domain: str) -> dict:
    """
    Fetches and normalizes federated user profile claims using Auth0's Userinfo endpoint.
    """
    userinfo_url = f"https://{auth0_domain}/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    profile_claims = response.json()

    # Normalize claims (example: rename 'sub' to 'user_id' for internal consistency)
    normalized_claims = {
        "user_id": profile_claims.get("sub"),
        "name": profile_claims.get("name"),
        "email": profile_claims.get("email"),
        "picture": profile_claims.get("picture"),
        "locale": profile_claims.get("locale"),
        "updated_at": profile_claims.get("updated_at"),
        **{k: v for k, v in profile_claims.items() if k not in ["sub", "name", "email", "picture", "locale", "updated_at"]}
    }
    return normalized_claims

if __name__ == 'main':
    # Example usage:
    # access_token = "YOUR_AUTH0_ACCESS_TOKEN"
    # auth0_domain = os.environ.get("AUTH0_DOMAIN") # e.g., dev-yourtenant.us.auth0.com
    #
    # try:
    #     user_profile = fetch_and_normalize_profile(access_token, auth0_domain)
    #     print("Normalized User Profile:", user_profile)
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error fetching user profile: {e}")
    #     print(e.response.json())
    pass
