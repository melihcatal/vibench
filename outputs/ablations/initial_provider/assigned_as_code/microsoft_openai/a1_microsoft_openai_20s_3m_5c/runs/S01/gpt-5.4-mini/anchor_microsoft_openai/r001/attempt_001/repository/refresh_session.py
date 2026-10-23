import msal

from identity_client import load_identity_config, require_config


def refresh_session(payload, config=None):
    config = require_config(load_identity_config(config), 'client_id', 'tenant_id', 'client_secret')
    app = msal.ConfidentialClientApplication(config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}", client_credential=config['client_secret'])
    result = app.acquire_token_by_refresh_token(payload['refresh_token'], scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in result:
        raise RuntimeError('Microsoft token refresh failed')
    return {'access_token': result['access_token'], 'expires_in': result.get('expires_in')}
