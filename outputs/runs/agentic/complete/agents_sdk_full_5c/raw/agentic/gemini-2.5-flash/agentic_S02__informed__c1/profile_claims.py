import os
import requests
import json

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

def fetch_user_profile(access_token: str):
    if not AUTH0_DOMAIN:
        raise ValueError("Missing Auth0_DOMAIN environment variable.")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    profile_claims = response.json()

    # Normalize claims (example: rename 'sub' to 'user_id' if needed)
    normalized_claims = {
        "user_id": profile_claims.get("sub"),
        "name": profile_claims.get("name"),
        "email": profile_claims.get("email"),
        "picture": profile_claims.get("picture"),
        **profile_claims  # Include all original claims as well
    }
    return normalized_claims

if __name__ == '__main__':
    # Example usage:
    # export AUTH0_DOMAIN="YOUR_AUTH0_DOMAIN"
    # access_t = "YOUR_ACCESS_TOKEN"
    # try:
    #     profile = fetch_user_profile(access_t)
    #     print("Fetched and normalized user profile:")
    #     print(json.dumps(profile, indent=2))
    # except Exception as e:
    #     print(f"Error fetching profile: {e}")
    pass
