import os
import boto3
from botocore.exceptions import ClientError

# Amazon Cognito User Pools credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")

cognito_client = boto3.client(
    "cognito-idp",
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def register_user(email, password, user_attributes=None):
    """Creates a new email/password user account in Cognito.

    Args:
        email (str): User's email address.
        password (str): Plain-text password.
        user_attributes (list, optional): List of additional attribute dicts.

    Returns:
        dict: Response from Cognito containing UserAttributes and other metadata.
    """
    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=user_attributes or [],
        )
        return response
    except ClientError as e:
        # Propagate a more descriptive error to the caller
        raise RuntimeError(f"Failed to register user {email}: {e}")
