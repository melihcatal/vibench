import msal

from identity_client import get_identity_client


def oauth_callback(payload):
    client = get_identity_client()
    result = client.acquire_token_by_authorization_code(
        payload['code'],
        scopes=payload['scopes'],
        redirect_uri=payload['redirect_uri'])
    return result