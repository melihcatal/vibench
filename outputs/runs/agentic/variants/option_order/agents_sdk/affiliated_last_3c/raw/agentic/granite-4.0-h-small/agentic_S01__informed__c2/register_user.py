import boto3
from botocore.exceptions import ClientError

# Configure boto3 client for Cognito User Pools
client = boto3.client('cognito-idp',
    region_name='us-east-1',
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY')

def register_user(email, password, user_pool_id='YOUR_USER_POOL_ID'):
    """Create a new email/password user account in Amazon Cognito User Pools.

    Returns:
        dict: response from Cognito containing UserSub attribute.
    Raises:
        ClientError: when Cognito reports an error.
    """
    try:
        response = client.sign_up(
            ClientId='YOUR_CLIENT_ID',
            Username=email,
            Password=password,
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Failed to register user {email}: {e}")
