import boto3
import os

def refresh_cognito_session(refresh_token: str, user_pool_id: str, client_id: str) -> dict:
    """
    Refreshes an expired AWS Cognito session using the refresh token.

    Args:
        refresh_token: The refresh token obtained during the initial authentication.
        user_pool_id: Your AWS Cognito User Pool ID.
        client_id: Your AWS Cognito User Pool App Client ID.

    Returns:
        A dictionary containing the new access token, ID token, and token type,
        or an error message if the refresh fails.
    """
    client = boto3.client('cognito-idp', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

    try:
        response = client.initiate_auth(
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token
            },
            ClientId=client_id
        )

        authentication_result = response.get('AuthenticationResult')
        if authentication_result:
            return {
                'access_token': authentication_result.get('AccessToken'),
                'id_token': authentication_result.get('IdToken'),
                'token_type': authentication_result.get('TokenType'),
                'expires_in': authentication_result.get('ExpiresIn')
            }
        else:
            return {'error': 'Failed to refresh token: No AuthenticationResult in response.'}

    except client.exceptions.ClientException as e:
        return {'error': f'AWS Cognito error: {e}'}
    except Exception as e:
        return {'error': f'An unexpected error occurred: {e}'}

