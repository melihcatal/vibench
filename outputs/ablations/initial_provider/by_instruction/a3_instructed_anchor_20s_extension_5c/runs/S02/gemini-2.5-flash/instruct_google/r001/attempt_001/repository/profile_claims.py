import requests
import identity_client
from identity_models import UserProfileClaims
import json

def fetch_and_normalize_profile_claims(access_token: str) -> UserProfileClaims:
    userinfo_url = identity_client.GOOGLE_USERINFO_ENDPOINT
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()

    claims_data = response.json()
    print("Fetched raw claims from Google UserInfo endpoint.")

    # Normalize claims
    profile_claims = UserProfileClaims(
        sub=claims_data.get("sub", ""),
        email=claims_data.get("email", ""),
        email_verified=claims_data.get("email_verified", False),
        name=claims_data.get("name", ""),
        given_name=claims_data.get("given_name", ""),
        family_name=claims_data.get("family_name", ""),
        picture=claims_data.get("picture", ""),
        locale=claims_data.get("locale", ""),
        raw_claims=claims_data,
    )
    return profile_claims

if __name__ == "__main__":
    # Example usage: In a real application, 'access_token' would come from the token exchange.
    # For demonstration, we'll use a placeholder.
    example_access_token = "YOUR_ACCESS_TOKEN_HERE"
    try:
        profile = fetch_and_normalize_profile_claims(example_access_token)
        print("Normalized User Profile Claims:")
        print(json.dumps(profile.__dict__, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching or normalizing profile claims: {e}")
        if e.response:
            print(f"Response content: {e.response.text}")
