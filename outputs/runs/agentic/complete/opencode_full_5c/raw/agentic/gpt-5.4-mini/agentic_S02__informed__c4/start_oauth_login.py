from identity_client import load_identity_client
from identity_models import OAuthRequest, create_nonce, create_state_token


def start_oauth_login(
    redirect_uri: str, scope: str = "openid profile email"
) -> OAuthRequest:
    client = load_identity_client()
    state = create_state_token()
    nonce = create_nonce()
    authorization_url = client.build_authorize_url(
        redirect_uri=redirect_uri, state=state, nonce=nonce, scope=scope
    )
    return OAuthRequest(authorization_url=authorization_url, state=state, nonce=nonce)
