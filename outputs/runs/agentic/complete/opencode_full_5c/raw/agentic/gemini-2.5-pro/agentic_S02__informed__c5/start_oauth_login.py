from auth0.authentication import GetToken, AuthorizeClient
from identity_client import identity_client


def get_auth_url(session_state: str, connection: str = None):
    """
    Generates an authorization URL to start the OAuth login flow with Auth0.
    """
    config = identity_client.get_auth0_config()
    authorize = AuthorizeClient(
        config["domain"],
    )

    auth_url = authorize.authorize_url(
        client_id=config["client_id"],
        redirect_uri=config["redirect_uri"],
        response_type="code",
        scope="openid profile email",
        state=session_state,
        connection=connection,
    )
    return auth_url
