import msal
import requests

from identity_client import load_identity_config
from identity_models import normalize_email, require_fields


def email_password_login(payload, config=None):
    payload = require_fields(payload, ['email', 'password'])
    config = load_identity_config(config)
    app = msal.PublicClientApplication(config['client_id'], authority='https://login.microsoftonline.com/' + config['tenant_id'])
    result = app.acquire_token_by_username_password(normalize_email(payload['email']), payload['password'], scopes=['openid', 'profile', 'offline_access'])
    if 'access_token' not in result:
        raise RuntimeError('Microsoft Entra login failed')
    return {'access_token': result['access_token'], 'refresh_token': result.get('refresh_token'), 'id_token': result.get('id_token'), 'token_type': result.get('token_type', 'Bearer')}
