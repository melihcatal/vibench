import requests
from identity_client import get_oauth_config, OAuthConfig
from identity_models import UserProfile


def fetch_normalized_profile(provider: str, access_token: str) -> UserProfile:
    config: OAuthConfig = get_oauth_config(provider)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(config.userinfo_url, headers=headers)
    response.raise_for_status()
    
    user_data = response.json()
    
    return UserProfile(
        sub=user_data.get("sub"),
        name=user_data.get("name"),
        given_name=user_data.get("given_name"),
        family_name=user_data.get("family_name"),
        email=user_data.get("email"),
        email_verified=user_data.get("email_verified", False),
        picture=user_data.get("picture"),
        locale=user_data.get("locale"),
    )