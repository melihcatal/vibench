import requests

from identity_client import get_client


def password_reset(email, config=None):
    client = get_client(config)
    token = client.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    response = requests.post('https://graph.microsoft.com/v1.0/users/{}/sendPasswordResetMail'.format(email),
        headers={'Authorization': 'Bearer ' + token['access_token']}, timeout=30)
    response.raise_for_status()
    return {'status': 'Password reset email sent'}