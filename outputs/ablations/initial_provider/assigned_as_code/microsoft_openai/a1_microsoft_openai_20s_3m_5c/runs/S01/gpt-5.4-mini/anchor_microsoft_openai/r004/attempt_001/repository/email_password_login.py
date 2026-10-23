import msal
import requests

from identity_client import authority_url, load_identity_config
from identity_models import normalize_email, parse_tokens


def email_password_login(payload, config=None):
    config = load_identity_config(config)
    app = msal.PublicClientApplication(config['client_id'], authority=authority_url(config))
    result = app.acquire_token_by_username_password(
        username=normalize_email(payload['email']),
        password=payload['password'],
        scopes=['openid', 'profile', 'offline_access'],
    )
    if 'access_token' not in result and 'refresh_token' not in result:
        token_url = f"{config['openid_base_url'].rstrip('/')}/{config['tenant_id']}/oauth2/v2.0/token"
        response = requests.post(token_url, data={
            'client_id': config['client_id'],
            'grant_type': 'password',
            'username': normalize_email(payload['email']),
            'password': payload['password'],
            'scope': 'openid profile offline_access',
        }, timeout=30)
        response.raise_for_status()
        result = response.json()
    return parse_tokens(result)
