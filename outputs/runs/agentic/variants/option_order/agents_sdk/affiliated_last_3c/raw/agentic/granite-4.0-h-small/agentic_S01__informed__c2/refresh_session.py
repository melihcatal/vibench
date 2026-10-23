import boto3
from botocore.exceptions import ClientError

cognito = boto3.client('cognito-idp',
    region_name='us-east-1',
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY')

def refresh_session(refresh_token, user_pool_id='YOUR_USER_POOL_ID'):
    """Exchange a refresh token for new access/id tokens.

    Returns:
        dict: response from Cognito containing new IdToken and RefreshToken.
    Raises:
        ClientError: if token refresh fails.
    """
    try:
        response = cognito.initiate_auth(
            ClientId='YOUR_CLIENT_ID',
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
            },
            AuthChallengeResponse={}
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Refresh failed: {e}")
