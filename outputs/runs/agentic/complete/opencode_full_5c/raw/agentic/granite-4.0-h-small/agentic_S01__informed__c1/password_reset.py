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


def initiate_password_reset(email):
    """Starts a password reset flow for a local Cognito user.

    Args:
        email (str): Registered user email.

    Returns:
        dict: Cognito response indicating a verification code was sent.
    """
    try:
        response = cognito_client.forgot_password(
            ClientId=CLIENT_ID,
            Username=email,
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Password reset request failed for {email}: {e}")


def confirm_password_reset(email, confirmation_code, new_password):
    """Confirms the password reset with the code and sets a new password.

    Args:
        email (str): Registered user email.
        confirmation_code (str): Code sent to the user.
        new_password (str): New password to assign.

    Returns:
        dict: Cognito response confirming password update.
    """
    try:
        response = cognito_client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=confirmation_code,
            Password=new_password,
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Password reset confirmation failed for {email}: {e}")
