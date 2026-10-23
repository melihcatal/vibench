import os
from botocore.exceptions import ClientError
from identity_client import get_cognito_client, COGNITO_CLIENT_ID
from identity_models import LoginCredentials, TokenResponse

def login_with_email_password(credentials: LoginCredentials) -> TokenResponse:
    """
    Signs in a user with email and password using Amazon Cognito.
    """
    cognito_client = get_cognito_client()
    
    if not COGNITO_CLIENT_ID:
        raise ValueError("COGNITO_CLIENT_ID environment variable is not set.")

    try:
        response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': credentials.email,
                'PASSWORD': credentials.password,
            }
        )
        
        auth_result = response['AuthenticationResult']
        return TokenResponse(
            access_token=auth_result['AccessToken'],
            refresh_token=auth_result.get('RefreshToken'),
            id_token=auth_result['IdToken'],
            token_type=auth_result['TokenType'],
            expires_in=auth_result['ExpiresIn']
        )
    except ClientError as e:
        # Handle exceptions, e.g., NotAuthorizedException
        print(f"Error logging in: {e}")
        raise
