import boto3
import os
from identity_client import IdentityClient


def refresh_session(refresh_token: str) -> dict:
    """Refreshes an expired session or access token using Amazon Cognito.

    Returns a dict with new tokens (IDToken, AccessToken, RefreshToken) or an error.
    """
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.refresh_tokens(
        RefreshToken=refresh_token, ClientId=os.getenv("COGNITO_CLIENT_ID")
    )
    return response  # contains Tokens: {IDToken, AccessToken, RefreshToken}
