import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# AWS credentials are expected in environment variables
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
client = boto3.client("cognito-idp")


def register_user(email, password, user_pool_id, client_id):
    """Create a new email/password user account using Amazon Cognito User Pools.

    Parameters:
        email (str): The user's email address.
        password (str): The user's password.
        user_pool_id (str): The target Cognito User Pool ID.
        client_id (str): The Cognito User Pool App Client ID.

    Returns:
        dict: The response from Cognito containing the new user's ARN and other metadata.
    """
    try:
        response = client.sign_up(
            ClientId=client_id,
            SecretHash=client.secret_hash(user_pool_id, client_id),
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}],
        )
        return response
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Cognito registration failed: {e}")
