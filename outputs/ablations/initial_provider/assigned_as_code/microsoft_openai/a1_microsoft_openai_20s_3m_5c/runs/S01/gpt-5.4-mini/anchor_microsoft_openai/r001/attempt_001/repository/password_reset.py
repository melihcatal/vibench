import msal
import requests

from identity_client import load_identity_config, require_config, graph_headers
from identity_models import normalize_email


def password_reset(payload, config=None):
    config = require_config(load_identity_config(config), 'client_id', 'tenant_id', 'client_secret', 'issuer')
    app = msal.ConfidentialClientApplication(config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}", client_credential=config['client_secret'])
    token = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    response = requests.post('https://graph.microsoft.com/v1.0/users', headers=graph_headers(token['access_token']), json={'identities': [{'signInType': 'emailAddress', 'issuer': config['issuer'], 'issuerAssignedId': normalize_email(payload['email'])}], 'passwordProfile': {'forceChangePasswordNextSignIn': True, 'password': payload['new_password']}}, timeout=30)
    response.raise_for_status()
    return {'user_id': response.json().get('id'), 'status': 'reset_started'}
