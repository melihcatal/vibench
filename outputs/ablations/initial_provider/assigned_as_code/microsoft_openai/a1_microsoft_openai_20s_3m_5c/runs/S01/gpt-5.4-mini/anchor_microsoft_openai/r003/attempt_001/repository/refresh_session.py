import msal

from identity_client import load_identity_config, require_config


def refresh_session(payload, config=None):
    config = load_identity_config(config)
    require_config(config, 'tenant_id', 'client_id', 'client_secret')
    app = msal.PublicClientApplication(config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")
    result = app.acquire_token_by_refresh_token(payload['refresh_token'], scopes=payload.get('scopes') or ['openid', 'profile', 'offline_access'])
    if 'access_token' not in result:
        raise RuntimeError('Session refresh failed')
    return {'access_token': result['access_token'], 'refresh_token': result.get('refresh_token', payload['refresh_token']), 'expires_in': result.get('expires_in')}
