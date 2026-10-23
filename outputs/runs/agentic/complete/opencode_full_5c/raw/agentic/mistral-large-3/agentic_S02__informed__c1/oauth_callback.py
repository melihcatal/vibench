import os
from identity_client import MicrosoftEntraIdentityClient
from identity_models import OAuthTokenResponse


def oauth_callback(
    redirect_uri: str, code: str, code_verifier: str
) -> OAuthTokenResponse:
    client = MicrosoftEntraIdentityClient()

    token_response = client.exchange_code_for_token(
        redirect_uri=redirect_uri, code=code, code_verifier=code_verifier
    )

    return OAuthTokenResponse(
        access_token=token_response.get("access_token"),
        id_token=token_response.get("id_token"),
        refresh_token=token_response.get("refresh_token"),
        expires_in=token_response.get("expires_in"),
        token_type=token_response.get("token_type"),
    )
