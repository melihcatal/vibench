import os
from botocore.exceptions import ClientError
from identity_client import get_cognito_client, COGNITO_CLIENT_ID
from identity_models import RefreshRequest, TokenResponse

def refresh_session_tokens(refresh_data: RefreshRequest) -> TokenResponse:
    """
    Refreshes an access token using a refresh token with Amazon Cognito.
    """
    cognito_client = get_cognito_client()

    if not COGNITO_CLIENT_ID:
        raise ValueError("COGNITO_CLIENT_ID environment variable is not set.")

    try:
        response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_data.refresh_token,
            }
        )
        
        auth_result = response['AuthenticationResult']
        # Cognito doesn't always return a new refresh token
        return TokenResponse(
            access_token=auth_result['AccessToken'],
            id_token=auth_result['IdToken'],
            token_type=auth_result['TokenType'],
            expires_in=auth_result['ExpiresIn']
        )
    except ClientError as e:
        # Handle exceptions, e.g., NotAuthorizedException
        print(f"Error refreshing session: {e}")
        raise
