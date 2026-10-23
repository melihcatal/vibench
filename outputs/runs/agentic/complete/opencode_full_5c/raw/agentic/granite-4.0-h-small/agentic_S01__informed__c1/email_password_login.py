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


def email_password_login(email, password):
    """Signs in a user with email and password, returning temporary credentials.

    Args:
        email (str): Registered user email.
        password (str): Plain-text password.

    Returns:
        dict: Cognito response containing AccessToken, IdToken, RefreshToken.
    """
    try:
        response = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Login failed for {email}: {e}")
