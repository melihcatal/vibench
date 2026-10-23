import os
from identity_client import CognitoClient
from identity_models import RefreshSessionRequest, AuthResponse


def refresh_session(payload: RefreshSessionRequest, config=None) -> AuthResponse:
    config = config or {}
    cognito_client = CognitoClient(
        region_name=config.get("region"),
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret")
    )

    auth_params = {
        "REFRESH_TOKEN": payload.refresh_token,
    }
    # No SecretHash needed for refresh_token flow

    response = cognito_client.client.initiate_auth(
        ClientId=cognito_client.client_id,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters=auth_params
    )

    if 'AuthenticationResult' in response:
        auth_result = response['AuthenticationResult']
        return AuthResponse(
            access_token=auth_result.get('AccessToken'),
            id_token=auth_result.get('IdToken'),
            refresh_token=payload.refresh_token, # Refresh token is usually not returned again
            expires_in=auth_result.get('ExpiresIn'),
            token_type=auth_result.get('TokenType')
        )
    return AuthResponse()
