import boto3
from botocore.exceptions import ClientError

cognito = boto3.client('cognito-idp',
    region_name='us-east-1',
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY')

def login_user(email, password, user_pool_id='YOUR_USER_POOL_ID'):
    """Sign in a user with email/password and return tokens.

    Returns:
        dict: response from Cognito containing IdToken and RefreshToken.
    Raises:
        ClientError: if authentication fails.
    """
    try:
        response = cognito.initiate_auth(
            ClientId='YOUR_CLIENT_ID',
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
            },
            AuthChallengeResponse={}
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Login failed for {email}: {e}")
