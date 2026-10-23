import msal

from identity_client import load_identity_config
from identity_models import require_fields


def refresh_session(payload, config=None):
    payload = require_fields(payload, ['refresh_token'])
    config = load_identity_config(config)
    app = msal.PublicClientApplication(config['client_id'], authority='https://login.microsoftonline.com/' + config['tenant_id'])
    result = app.acquire_token_by_refresh_token(payload['refresh_token'], scopes=['openid', 'profile', 'offline_access'])
    if 'access_token' not in result:
        raise RuntimeError('Microsoft Entra refresh failed')
    return {'access_token': result['access_token'], 'refresh_token': result.get('refresh_token', payload['refresh_token']), 'id_token': result.get('id_token'), 'token_type': result.get('token_type', 'Bearer')}
