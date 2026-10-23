import requests
from.identity_client import get_identity_client


def oauth_callback(authorization_code, session_id, config):
    client = get_identity_client(config)
    token_endpoint = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': config['client_id'],
        'redirect_uri': config['redirect_uri'],
        'code': authorization_code,
        'client_secret': config['client_secret']
    }
    response = client.post(token_endpoint, data=data)
    response.raise_for_status()
    return response.json()