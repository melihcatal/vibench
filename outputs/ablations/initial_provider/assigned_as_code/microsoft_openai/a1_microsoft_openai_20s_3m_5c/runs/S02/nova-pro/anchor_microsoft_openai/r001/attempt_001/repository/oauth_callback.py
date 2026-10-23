import msal

from identity_client import get_identity_client


def handle_oauth_callback(payload):
    app = get_identity_client()
    result = app.acquire_token_by_authorization_code(
        payload['code'],
        scopes=payload.get('scopes', ['User.Read']),
        redirect_uri=payload['redirect_uri'])
    return result