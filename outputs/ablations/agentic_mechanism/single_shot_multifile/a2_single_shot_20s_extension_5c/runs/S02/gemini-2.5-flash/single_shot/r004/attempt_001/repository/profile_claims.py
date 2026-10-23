import os
import requests

from identity_client import OKTA_ORG_URL
from identity_models import UserProfileClaims

def fetch_okta_user_profile(access_token: str) -> UserProfileClaims:
    """Fetches user profile claims from Okta's /userinfo endpoint."""
    userinfo_endpoint = f"{OKTA_ORG_URL}/oauth2/default/v1/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    response = requests.get(userinfo_endpoint, headers=headers)
    response.raise_for_status()
    claims_data = response.json()

    # Normalize claims into our UserProfileClaims model
    profile = UserProfileClaims(
        sub=claims_data.get('sub'),
        name=claims_data.get('name'),
        email=claims_data.get('email'),
        email_verified=claims_data.get('email_verified'),
        given_name=claims_data.get('given_name'),
        family_name=claims_data.get('family_name'),
        preferred_username=claims_data.get('preferred_username'),
        zoneinfo=claims_data.get('zoneinfo'),
        locale=claims_data.get('locale'),
        picture=claims_data.get('picture'),
        updated_at=claims_data.get('updated_at')
    )
    return profile
