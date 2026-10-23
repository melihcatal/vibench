import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# AWS credentials are expected in environment variables
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
client = boto3.client("cognito-idp")


def email_password_login(email, password, user_pool_id, client_id):
    """Sign in a user with email and password and return authentication tokens.

    Parameters:
        email (str): The user's email address.
        password (str): The user's password.
        user_pool_id (str): The target Cognito User Pool ID.
        client_id (str): The Cognito User Pool App Client ID.

    Returns:
        dict: Tokens (id_token, access_token, refresh_token) and user metadata.
    """
    try:
        # First make sure the user exists and confirm if needed
        user = client.admin_get_user(UserPoolId=user_pool_id, Username=email)
        if not user.get("Enabled", False):
            raise RuntimeError("User is not enabled")

        auth_response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        return auth_response
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Cognito login failed: {e}")
