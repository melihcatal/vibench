import msal
import requests

def login_user(email, password, config=None):
    config = config or {}
    app = msal.PublicClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")
    result = app.acquire_token_by_username_password(
        username=email, password=password, scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in result:
        raise RuntimeError('Microsoft Graph authentication failed')
    return result