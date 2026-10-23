import requests
from identity_client import IdentityClientConfig
from identity_models import UserProfile

def fetch_auth0_user_profile(access_token: str) -> UserProfile:
    userinfo_url = f"https://{{IdentityClientConfig.AUTH0_DOMAIN}}/userinfo"
    headers = {
        "Authorization": f"Bearer {{access_token}}"
    }
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    profile_data = response.json()

    return UserProfile(
        sub=profile_data.get("sub"),
        name=profile_data.get("name"),
        email=profile_data.get("email"),
        email_verified=profile_data.get("email_verified"),
        picture=profile_data.get("picture"),
        locale=profile_data.get("locale"),
        raw_claims=profile_data
    )

if __name__ == "__main__":
    # Example usage. In a real scenario, access_token would come from oauth_callback.py
    # For demonstration, use a dummy token (this will likely fail without a real one).
    dummy_access_token = "YOUR_AUTH0_ACCESS_TOKEN_HERE"
    try:
        # profile = fetch_auth0_user_profile(dummy_access_token)
        # print(f"Fetched user profile: {profile}")
        print("To test this, you need a valid Auth0 access token.")
        print("Ensure AUTH0_DOMAIN is set.")
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching user profile: {e}")
        print(f"Response: {e.response.text}")
