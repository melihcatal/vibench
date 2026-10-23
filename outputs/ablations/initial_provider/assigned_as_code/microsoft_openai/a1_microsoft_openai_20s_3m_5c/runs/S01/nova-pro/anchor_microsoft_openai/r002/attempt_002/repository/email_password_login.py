import msal
import requests


def login_user(email, password, config=None):
    config = config or {}
    app = msal.PublicClientApplication(config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")
    token = app.acquire_token_by_username_password(username=email, password=password, scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    return {'access_token': token['access_token'], 'refresh_token': token['refresh_token']}
