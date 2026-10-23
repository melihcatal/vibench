from identity_client import get_auth0_client, get_auth0_config
from identity_models import TokenResponse

def handle_auth0_callback(code: str) -> TokenResponse:
    """
    Handles the callback from Auth0, exchanging an authorization code for tokens.

    Args:
        code: The authorization code received from Auth0.

    Returns:
        A dictionary containing the access token, ID token, and other token data.
    """
    auth0_client = get_auth0_client()
    config = get_auth0_config()

    token_data = auth0_client.get_token_by_authorization_code(
        code=code,
        redirect_uri=config["callback_url"]
    )
    return token_data
