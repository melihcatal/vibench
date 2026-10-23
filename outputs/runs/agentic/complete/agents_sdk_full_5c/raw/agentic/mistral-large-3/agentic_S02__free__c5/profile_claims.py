from identity_client import get_oauth_config
import requests
from identity_models import NormalizedProfile

def fetch_normalized_profile(provider_name: str, access_token: str) -> NormalizedProfile:
    config = get_oauth_config(provider_name)
    if not config:
        raise ValueError(f"Unsupported provider: {provider_name}")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }

    response = requests.get(config['userinfo_url'], headers=headers)
    response.raise_for_status()
    userinfo = response.json()

    # Normalize claims for Google Identity Platform
    return NormalizedProfile(
        sub=userinfo.get('sub'),
        name=userinfo.get('name'),
        given_name=userinfo.get('given_name'),
        family_name=userinfo.get('family_name'),
        email=userinfo.get('email'),
        email_verified=userinfo.get('email_verified', False),
        picture=userinfo.get('picture'),
        locale=userinfo.get('locale'),
        provider=provider_name,
    )