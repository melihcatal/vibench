import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# AWS credentials are expected in environment variables
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
client = boto3.client("cognito-idp")


def refresh_session(refresh_token, user_pool_id, client_id):
    """
    Refresh an expired session or access token using Amazon Cognito.

    Parameters:
        refresh_token (str): The refresh token obtained from a previous login.
        user_pool_id (str): The target Cognito User Pool ID.
        client_id (str): The Cognito User Pool App Client ID.

    Returns:
        dict: New tokens (id_token, access_token, refresh_token) if refresh succeeds.
    """
    try:
        # AdminInitiateAuth can be used with REFRESH_TOKEN_AUTH flow
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": refresh_token},
        )
        return response
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Cognito token refresh failed: {e}")
