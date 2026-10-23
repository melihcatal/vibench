import requests
from.identity_client import get_identity_client


def fetch_profile_claims(access_token, config):
    client = get_identity_client(config)
    userinfo_endpoint = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/userInfo"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.get(userinfo_endpoint, headers=headers)
    response.raise_for_status()
    claims = response.json()
    normalized_claims = {
        'sub': claims.get('sub', ''),
        'name': claims.get('name', ''),
        'email': claims.get('email', ''),
        'picture': claims.get('picture', '')
    }
    return normalized_claims