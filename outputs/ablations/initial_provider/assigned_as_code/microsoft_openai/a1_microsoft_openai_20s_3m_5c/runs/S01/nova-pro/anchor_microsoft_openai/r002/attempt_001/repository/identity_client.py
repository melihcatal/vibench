import msal
import requests

def get_identity_client(config):
    app = msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
    return app

def get_access_token(app, scopes):
    token = app.acquire_token_for_client(scopes=scopes)
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    return token['access_token']