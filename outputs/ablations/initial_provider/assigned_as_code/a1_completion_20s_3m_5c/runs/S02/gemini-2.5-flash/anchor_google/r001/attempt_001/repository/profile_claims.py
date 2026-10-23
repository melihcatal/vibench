import requests
from identity_models import UserProfileClaims
from identity_client import GoogleIdentityProviderClient

def fetch_and_normalize_profile_claims(access_token: str) -> UserProfileClaims:
    client = GoogleIdentityProviderClient()

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(client.get_userinfo_url(), headers=headers, timeout=30)
    response.raise_for_status()
    claims_data = response.json()

    return UserProfileClaims(
        sub=claims_data.get("sub"),
        email=claims_data.get("email"),
        email_verified=claims_data.get("email_verified"),
        name=claims_data.get("name"),
        given_name=claims_data.get("given_name"),
        family_name=claims_data.get("family_name"),
        picture=claims_data.get("picture"),
        locale=claims_data.get("locale"),
        claims_raw=claims_data
    )
