import os
import webbrowser
from identity_client import build_authorize_url

def start_oauth_login(redirect_uri: str, scope: str = 'openid profile email', state: str = None):
    domain = os.getenv('AUTH0_DOMAIN')
    if not domain:
        raise ValueError("AUTH0_DOMAIN environment variable not set")
    client_id = os.getenv('AUTH0_CLIENT_ID')
    if not client_id:
        raise ValueError("AUTH0_CLIENT_ID environment variable not set")
    authorize_endpoint = f"https://{domain}/authorize"
    auth_url = build_authorize_url(authorize_endpoint, client_id, redirect_uri, scope, state)
    webbrowser.open(auth_url)
    print(f"OAuth login started: {auth_url}")
    return auth_url
