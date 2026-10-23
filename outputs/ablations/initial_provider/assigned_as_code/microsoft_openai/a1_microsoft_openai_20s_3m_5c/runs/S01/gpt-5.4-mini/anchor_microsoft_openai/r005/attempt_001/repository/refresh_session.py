import msal

from identity_client import load_identity_config


def refresh_session(payload, config=None):
    config = load_identity_config(config)
    payload = payload or {}
    app = msal.ConfidentialClientApplication(
        config.client_id,
        authority=f'https://login.microsoftonline.com/{config.tenant_id}',
        client_credential=config.client_secret,
    )
    token = app.acquire_token_silent(['https://graph.microsoft.com/.default'], account=None)
    if not token or 'access_token' not in token:
        token = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph session refresh failed')
    return {'access_token': token['access_token'], 'refresh_token': token.get('refresh_token', payload.get('refresh_token', ''))}
