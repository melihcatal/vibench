import requests
from identity_client import get_provider_config
from identity_models import UserProfileClaims

def fetch_user_profile_claims(access_token: str) -> UserProfileClaims:
    provider_config = get_provider_config()
    userinfo_endpoint = provider_config.get("userinfo_endpoint")

    if not userinfo_endpoint:
        raise ValueError("OAUTH_USERINFO_ENDPOINT not found in provider configuration")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_endpoint, headers=headers, timeout=30)
    response.raise_for_status()
    claims_data = response.json()

    return UserProfileClaims(
        sub=claims_data.get("sub"),
        name=claims_data.get("name"),
        given_name=claims_data.get("given_name"),
        family_name=claims_data.get("family_name"),
        nickname=claims_data.get("nickname"),
        picture=claims_data.get("picture"),
        email=claims_data.get("email"),
        email_verified=claims_data.get("email_verified"),
    )
