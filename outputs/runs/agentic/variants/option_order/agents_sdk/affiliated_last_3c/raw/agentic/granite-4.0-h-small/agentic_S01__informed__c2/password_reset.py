import boto3
from botocore.exceptions import ClientError

cognito = boto3.client('cognito-idp',
    region_name='us-east-1',
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY')

def initiate_password_reset(email, user_pool_id='YOUR_USER_POOL_ID'):
    """Start a password reset flow for a local Cognito user.

    Returns:
        dict: response from Cognito containing a ResetPasswordCode.
    Raises:
        ClientError: if the request fails.
    """
    try:
        response = cognito.forgot_password(
            ClientId='YOUR_CLIENT_ID',
            Username=email
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Password reset initiation failed for {email}: {e}")
