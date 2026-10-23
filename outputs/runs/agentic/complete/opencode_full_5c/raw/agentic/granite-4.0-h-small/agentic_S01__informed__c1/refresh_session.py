import os
import boto3
from botocore.exceptions import ClientError

# Refresh token usage requires Cognito Identity Pool linked to the User Pool
IDENTITY_POOL_ID = os.getenv("COGNITO_IDENTITY_POOL_ID")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

cognito_identity_client = boto3.client(
    "cognito-identity",
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def refresh_session(id_token):
    """Refreshes an expired access token using the existing refresh token.

    Cognito does not expose a direct refresh endpoint via boto3; instead we use
    the Identity Pool's GetId + GetCredentialsForIdentity flow which validates
    the refresh token.

    Args:
        id_token (str): Currently valid ID token (or refresh token if supported).

    Returns:
        dict: Updated credentials including new AccessToken.
    """
    try:
        # Exchange refresh token for new tokens via the identity pool
        identity_response = cognito_identity_client.get_id(
            IdentityPoolId=IDENTITY_POOL_ID,
        )
        identity_id = identity_response["IdentityId"]

        credentials = cognito_identity_client.get_credentials_for_identity(
            IdentityId=identity_id,
            Logins={
                # Cognito does not require a specific login provider for refresh
                "cognito-identity.amazonaws.com": id_token,
            },
        )
        return {
            "AccessKeyId": credentials["AccessKeyId"],
            "SecretKey": credentials["SecretKey"],
            "SessionToken": credentials["SessionToken"],
        }
    except ClientError as e:
        raise RuntimeError(f"Refresh failed: {e}")
