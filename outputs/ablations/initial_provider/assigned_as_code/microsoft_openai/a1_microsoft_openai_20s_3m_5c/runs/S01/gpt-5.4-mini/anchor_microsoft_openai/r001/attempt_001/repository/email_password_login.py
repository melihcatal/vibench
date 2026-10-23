import msal
import requests

from identity_client import load_identity_config, require_config
from identity_models import normalize_email


def email_password_login(payload, config=None):
    config = require_config(load_identity_config(config), 'client_id', 'tenant_id')
    app = msal.PublicClientApplication(config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")
    result = app.acquire_token_by_username_password(normalize_email(payload['email']), payload['password'], scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in result:
        raise RuntimeError('Microsoft identity login failed')
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers={'Authorization': 'Bearer ' + result['access_token']}, timeout=30)
    response.raise_for_status()
    return {'access_token': result['access_token'], 'refresh_token': result.get('refresh_token'), 'profile': response.json()}
