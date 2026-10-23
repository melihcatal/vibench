import os
import requests
import json
from identity_client import get_auth0_config
from identity_models import UserProfileClaims

def fetch_and_normalize_auth0_profile(access_token: str):
    config = get_auth0_config()
    domain = config["AUTH0_DOMAIN"]

    userinfo_url = f"https://{domain}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        raw_claims = response.json()

        normalized_claims = UserProfileClaims(
            sub=raw_claims.get("sub"),
            name=raw_claims.get("name"),
            email=raw_claims.get("email"),
            email_verified=raw_claims.get("email_verified"),
            picture=raw_claims.get("picture"),
            # Add other relevant claims
            raw_data=raw_claims
        )
        print("Successfully fetched and normalized user profile claims.")
        return normalized_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user profile: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with an actual access token)
    sample_access_token = os.environ.get("AUTH0_SAMPLE_ACCESS_TOKEN", "dummy_access_token")
    if sample_access_token == "dummy_access_token":
        print("Please set the AUTH0_SAMPLE_ACCESS_TOKEN environment variable with a real access token.")
    else:
        profile = fetch_and_normalize_auth0_profile(sample_access_token)
        if profile:
            print(json.dumps(profile.to_dict(), indent=2))
