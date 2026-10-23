import requests
import json
from typing import Optional

import identity_client
from identity_models import UserProfileClaims

def fetch_and_normalize_profile_claims(access_token: str) -> Optional[UserProfileClaims]:
    """Fetches user profile claims from Microsoft Graph and normalizes them."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(identity_client.AZURE_AD_GRAPH_ENDPOINT, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors

        profile_data = response.json()

        # Normalize claims
        normalized_claims = UserProfileClaims(
            sub=profile_data.get("id") or profile_data.get("oid", ""), # 'id' for /me, 'oid' for /users/{id}
            name=profile_data.get("displayName"),
            given_name=profile_data.get("givenName"),
            family_name=profile_data.get("surname"),
            email=profile_data.get("mail") or profile_data.get("userPrincipalName"),
            email_verified=True, # Microsoft Graph usually implies verified for mail field
            picture=None, # Microsoft Graph doesn't directly provide a picture URL in /me endpoint by default
            locale=profile_data.get("preferredLanguage"),
            raw_claims=profile_data
        )
        print("Successfully fetched and normalized user profile claims.")
        return normalized_claims

    except requests.exceptions.RequestException as e:
        print(f"Error fetching profile claims from Microsoft Graph: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return None

if __name__ == "__main__":
    # For demonstration, you would get an access token from oauth_callback.py
    print("Please provide a valid access token to test this script.")
    example_access_token = os.environ.get("OAUTH_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")

    if example_access_token == "YOUR_ACCESS_TOKEN_HERE":
        print("Please set the OAUTH_ACCESS_TOKEN environment variable or replace the placeholder.")
    else:
        print(f"Attempting to fetch claims with access token (first 20 chars): {example_access_token[:20]}...")
        claims = fetch_and_normalize_profile_claims(example_access_token)
        if claims:
            print(f"User Subject: {claims.sub}")
            print(f"User Name: {claims.name}")
            print(f"User Email: {claims.email}")
            print(f"Raw Claims: {json.dumps(claims.raw_claims, indent=2)}")
