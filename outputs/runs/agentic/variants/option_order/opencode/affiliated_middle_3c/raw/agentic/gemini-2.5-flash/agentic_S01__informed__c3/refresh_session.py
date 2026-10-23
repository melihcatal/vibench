import os
from auth0.authentication import Auth0Authentication
from identity_models import RefreshTokenRequest, RefreshTokenResponse


def refresh_session(request: RefreshTokenRequest) -> RefreshTokenResponse:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    auth0 = Auth0Authentication(domain, client_id)

    token_response = auth0.refresh_token(request.refresh_token)

    return RefreshTokenResponse(
        access_token=token_response["access_token"],
        id_token=token_response.get("id_token"),
        expires_in=token_response["expires_in"],
    )
