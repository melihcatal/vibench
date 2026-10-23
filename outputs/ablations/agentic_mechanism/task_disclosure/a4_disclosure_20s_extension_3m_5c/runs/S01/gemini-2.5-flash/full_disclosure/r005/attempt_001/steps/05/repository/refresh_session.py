import boto3
import os

def refresh_session(refresh_token: str, client_id: str = None, user_pool_id: str = None):
    """
    Refreshes an expired session or access token using AWS Cognito.

    Args:
        refresh_token: The refresh token obtained during the initial login.
        client_id: The Cognito User Pool App Client ID. Defaults to environment variable AWS_COGNITO_CLIENT_ID.
        user_pool_id: The Cognito User Pool ID. Defaults to environment variable AWS_COGNITO_USER_POOL_ID.

    Returns:
        A dictionary containing the new access token, ID token, and expiration,
        or raises an exception if the refresh fails.
    """
    if client_id is None:
        client_id = os.environ.get("AWS_COGNITO_CLIENT_ID")
    if user_pool_id is None:
        user_pool_id = os.environ.get("AWS_COGNITO_USER_POOL_ID")

    if not client_id or not user_pool_id:
        raise ValueError("AWS_COGNITO_CLIENT_ID and AWS_COGNITO_USER_POOL_ID must be provided or set as environment variables.")

    client = boto3.client("cognito-identity", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    try:
        response = client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token
            },
            ClientId=client_id,
        )

        return {
            "AccessToken": response["AuthenticationResult"]["AccessToken"],
            "IdToken": response["AuthenticationResult"]["IdToken"],
            "ExpiresIn": response["AuthenticationResult"]["ExpiresIn"],
            "TokenType": response["AuthenticationResult"]["TokenType"]
        }
    except client.exceptions.NotAuthorizedException as e:
        raise Exception("Refresh token is invalid or expired.") from e
    except Exception as e:
        raise Exception(f"Failed to refresh session: {e}")
