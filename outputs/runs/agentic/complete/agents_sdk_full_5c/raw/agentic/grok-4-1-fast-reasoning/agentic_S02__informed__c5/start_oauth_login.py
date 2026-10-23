import os
import webbrowser
from urllib.parse import urlencode
from identity_client import get_config

def start_oauth_login(redirect_uri: str = 'http://localhost:8080/callback'):
    tenant_id = os.getenv('AZURE_TENANT_ID')
    config = get_config()
    params = {
        'client_id': config['client_id'],
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': config['scopes'],
        'state': 'randomstate123',
    }
    auth_url = f"{config['authority']}/authorize?{urlencode(params)}"
    print(f"Visit this URL to login: {auth_url}")
    webbrowser.open(auth_url)