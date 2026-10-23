import requests

from identity_client import get_cognito_client


def fetch_profile_claims(access_token, config=None):
    config = config or {}
    client = get_cognito_client(config)
    userinfo_endpoint = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/userInfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = client.get(userinfo_endpoint, headers=headers)
    userinfo_data = userinfo_response.json()
    return userinfo_data