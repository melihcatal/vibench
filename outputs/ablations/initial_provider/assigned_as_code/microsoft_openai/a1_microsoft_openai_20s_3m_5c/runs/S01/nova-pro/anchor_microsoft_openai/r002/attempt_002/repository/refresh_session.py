import msal
import requests


def refresh_session(refresh_token, config=None):
    config = config or {}
    app = msal.ConfidentialClientApplication(config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}", client_credential=config['client_secret'])
    token = app.acquire_token_by_refresh_token(refresh_token, scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    return {'access_token': token['access_token'], 'refresh_token': token['refresh_token']}
