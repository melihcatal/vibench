import msal
import requests

from identity_client import load_identity_config, require_config
from identity_models import build_email_password_payload


def email_password_login(payload, config=None):
    config = load_identity_config(config)
    require_config(config, 'tenant_id', 'client_id', 'client_secret', 'issuer')
    payload = build_email_password_payload(payload)
    app = msal.PublicClientApplication(config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")
    token = app.acquire_token_by_username_password(payload['email'], payload['password'], scopes=['openid', 'profile', 'offline_access'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Entra login failed')
    return {'access_token': token['access_token'], 'refresh_token': token.get('refresh_token'), 'id_token': token.get('id_token'), 'expires_in': token.get('expires_in')}
