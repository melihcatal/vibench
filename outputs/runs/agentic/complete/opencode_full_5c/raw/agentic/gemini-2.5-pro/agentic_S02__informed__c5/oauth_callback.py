from auth0.authentication import GetToken
from identity_client import identity_client
from identity_models import OAuthTokenResponse


def exchange_code_for_token(authorization_code: str) -> OAuthTokenResponse:
    """
    Exchanges an authorization code for an access token and ID token from Auth0.
    """
    config = identity_client.get_auth0_config()
    get_token = GetToken(config["domain"])

    token_data = get_token.authorization_code(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        code=authorization_code,
        redirect_uri=config["redirect_uri"],
    )

    return OAuthTokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        token_type=token_data.get("token_type"),
        expires_in=token_data.get("expires_in"),
        scope=token_data.get("scope"),
        refresh_token=token_data.get("refresh_token"),
    )
