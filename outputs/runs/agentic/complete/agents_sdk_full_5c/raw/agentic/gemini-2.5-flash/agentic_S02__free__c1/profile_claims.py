import requests
from typing import Dict, Any

from identity_client import OKTA_ORG_URL
from identity_models import UserProfileClaims

def fetch_and_normalize_profile_claims(access_token: str) -> UserProfileClaims:
    """
    Fetches user profile claims from the Okta /userinfo endpoint
    and normalizes them into a standard format.
    """
    userinfo_url = f"{OKTA_ORG_URL}/oauth2/default/v1/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        claims_data = response.json()

        # Normalize claims
        normalized_claims = UserProfileClaims(
            sub=claims_data.get("sub"),
            name=claims_data.get("name", f"{claims_data.get("given_name", "")} {claims_data.get("family_name", "")}".strip()),
            given_name=claims_data.get("given_name"),
            family_name=claims_data.get("family_name"),
            email=claims_data.get("email"),
            email_verified=claims_data.get("email_verified"),
            picture=claims_data.get("picture"),
            locale=claims_data.get("locale"),
            zoneinfo=claims_data.get("zoneinfo"),
            updated_at=claims_data.get("updated_at"),
            # Add any other relevant claims from Okta
            okta_profile_id=claims_data.get("uid"), # Okta-specific ID
            preferred_username=claims_data.get("preferred_username")
        )
        print("Successfully fetched and normalized user profile claims.")
        return normalized_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info from Okta: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        raise

if __name__ == "__main__":
    # Example usage (replace with a valid access token)
    example_access_token = "YOUR_ACCESS_TOKEN_HERE"

    if "YOUR_ACCESS_TOKEN_HERE" in example_access_token:
        print("Please replace 'YOUR_ACCESS_TOKEN_HERE' with an actual access token obtained from the Okta callback.")
    else:
        try:
            profile_claims = fetch_and_normalize_profile_claims(example_access_token)
            print("Normalized Profile Claims:")
            print(profile_claims.to_dict()) # Assuming a to_dict method in UserProfileClaims
        except Exception as e:
            print(f"Failed to fetch profile claims: {e}")
