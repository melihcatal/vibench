import os
import boto3


def refresh_session(refresh_token: str) -> dict:
    """Refresh session or access token using Amazon Cognito refresh token.
    Returns new tokens (access_token, id_token, refresh_token) on success.
    """
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    response = client.refresh_token(RefreshToken=refresh_token)
    return response
