import os
from identity_client import IdentityClient
from identity_models import OAuthTokenResponse


def handle_oauth_callback(code: str, state: str, redirect_uri: str, session_id: str, code_verifier: str = None):
    # In a real application, you would verify the 'state' here against the stored session_id
    # to prevent CSRF attacks.
    if state != session_id:
        raise ValueError("State mismatch: Possible CSRF attack.")

    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Google client ID and client secret must be set as environment variables.")

    identity_client = IdentityClient(client_id, client_secret, redirect_uri)
    token_data = identity_client.exchange_authorization_code(code, code_verifier)
    return OAuthTokenResponse(**token_data)
