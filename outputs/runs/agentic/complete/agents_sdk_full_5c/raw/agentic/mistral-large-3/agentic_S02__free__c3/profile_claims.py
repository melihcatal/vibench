import requests
from identity_models import UserProfile
from identity_client import get_oauth_config, OAuthConfig


def fetch_user_profile(provider: str, access_token: str) -> UserProfile:
    config: OAuthConfig = get_oauth_config(provider)
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    response = requests.get(f"https://{config.domain}/userinfo", headers=headers)
    response.raise_for_status()
    
    user_data = response.json()
    
    return UserProfile(
        sub=user_data.get("sub"),
        name=user_data.get("name"),
        email=user_data.get("email"),
        email_verified=user_data.get("email_verified", False),
        picture=user_data.get("picture"),
        locale=user_data.get("locale"),
        provider=provider,
    )