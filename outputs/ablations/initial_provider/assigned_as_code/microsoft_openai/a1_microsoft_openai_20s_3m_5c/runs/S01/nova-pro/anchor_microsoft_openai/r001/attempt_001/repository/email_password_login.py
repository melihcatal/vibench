import msal
import requests

from identity_client import get_client


def email_password_login(email, password, config=None):
    client = get_client(config)
    token = client.acquire_token_by_username_password(username=email, password=password, scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph authentication failed')
    return token