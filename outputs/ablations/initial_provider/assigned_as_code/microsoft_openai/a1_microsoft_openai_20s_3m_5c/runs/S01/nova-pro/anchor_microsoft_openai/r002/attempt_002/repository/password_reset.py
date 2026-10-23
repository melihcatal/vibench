import msal
import requests


def start_password_reset(email, config=None):
    config = config or {}
    app = msal.ConfidentialClientApplication(config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}", client_credential=config['client_secret'])
    token = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    response = requests.post(f'https://graph.microsoft.com/v1.0/users/{email}/sendPasswordReset',
        headers={'Authorization': 'Bearer ' + token['access_token']}, timeout=30)
    response.raise_for_status()
    return {'status': 'Password reset email sent'}
