import msal
import requests

from identity_client import load_identity_config
from identity_models import build_email_password_payload


def email_password_login(payload, config=None):
    config = load_identity_config(config)
    payload = build_email_password_payload(payload)
    app = msal.ConfidentialClientApplication(
        config.client_id,
        authority=f'https://login.microsoftonline.com/{config.tenant_id}',
        client_credential=config.client_secret,
    )
    token = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    response = requests.post(
        'https://graph.microsoft.com/v1.0/me/validatePassword',
        headers={'Authorization': 'Bearer ' + token['access_token']},
        json={'email': payload['email'], 'password': payload['password']},
        timeout=30,
    )
    response.raise_for_status()
    return {'access_token': token['access_token'], 'refresh_token': token.get('refresh_token', ''), 'user': response.json()}
