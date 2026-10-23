import msal

from identity_client import get_client


def refresh_session(refresh_token, config=None):
    client = get_client(config)
    token = client.acquire_token_by_refresh_token(refresh_token=refresh_token, scopes=['https://graph.microsoft.com/.default'])
    if 'access_token' not in token:
        raise RuntimeError('Microsoft Graph token refresh failed')
    return token