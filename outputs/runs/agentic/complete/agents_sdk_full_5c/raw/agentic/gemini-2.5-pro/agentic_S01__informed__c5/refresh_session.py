from identity_client import get_identity_client, get_client_id
from identity_models import RefreshRequest, AuthTokens

def refresh_session_tokens(refresh_request: RefreshRequest) -> AuthTokens:
    """
    Refreshes an access token using a refresh token with Amazon Cognito.
    """
    client = get_identity_client()
    client_id = get_client_id()

    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_request.refresh_token
        }
    )

    auth_result = response['AuthenticationResult']
    return AuthTokens(
        access_token=auth_result['AccessToken'],
        id_token=auth_result['IdToken'],
        refresh_token=refresh_request.refresh_token # Cognito doesn't return a new one in this flow
    )
