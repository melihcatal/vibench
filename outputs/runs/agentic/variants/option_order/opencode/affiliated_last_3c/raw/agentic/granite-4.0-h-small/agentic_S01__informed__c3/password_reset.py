import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# AWS credentials are expected in environment variables
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
client = boto3.client("cognito-idp")


def start_password_reset(email, user_pool_id, client_id):
    """Initiate a password reset flow for a local email/password account.

    Parameters:
        email (str): The user's email address.
        user_pool_id (str): The target Cognito User Pool ID.
        client_id (str): The Cognito User Pool App Client ID.

    Returns:
        dict: Response containing a ChallengeName (usually 'NEW_PASSWORD_REQUIRED').
    """
    try:
        # First make sure the user exists and is confirmed
        user = client.admin_get_user(UserPoolId=user_pool_id, Username=email)
        if not user.get("Enabled", False):
            raise RuntimeError("User is not enabled")
        if not user.get("UserStatus", "") == "CONFIRMED":
            raise RuntimeError("User not confirmed")

        # Start the forgot password flow
        response = client.forgot_password(ClientId=client_id, Username=email)
        return response
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Cognito password reset initiation failed: {e}")
