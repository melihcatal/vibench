import requests

from identity_client import load_identity_config
from identity_models import parse_tokens


def refresh_session(payload, config=None):
    config = load_identity_config(config)
    token_url = f"{config['openid_base_url'].rstrip('/')}/{config['tenant_id']}/oauth2/v2.0/token"
    response = requests.post(token_url, data={
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'grant_type': 'refresh_token',
        'refresh_token': payload['refresh_token'],
        'scope': 'openid profile offline_access',
    }, timeout=30)
    response.raise_for_status()
    return parse_tokens(response.json())
