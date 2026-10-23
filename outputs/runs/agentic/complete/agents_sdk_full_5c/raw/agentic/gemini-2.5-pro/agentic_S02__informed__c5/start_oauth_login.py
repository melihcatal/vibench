from identity_client import get_auth0_client, get_auth0_config

def start_auth0_login(state: str, connection: str = None) -> str:
    """
    Starts an Auth0 OIDC login flow by generating an authorization URL.

    Args:
        state: An opaque value used to maintain state between the request and callback.
        connection: The name of the connection to use (e.g., 'google-oauth2').

    Returns:
        The authorization URL to redirect the user to.
    """
    auth0_client = get_auth0_client()
    config = get_auth0_config()
    
    authorize_url = auth0_client.get_authorize_url(
        redirect_uri=config["callback_url"],
        state=state,
        response_type="code",
        scope="openid profile email",
        connection=connection
    )
    return authorize_url
