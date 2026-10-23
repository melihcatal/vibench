import os
import boto3

def refresh_session(refresh_token: str) -> dict:
    """
    Refreshes an expired session or access token using AWS Cognito.

    Args:
        refresh_token: The refresh token to use for renewing the session.

    Returns:
        A dictionary containing the new access token, ID token, and refresh token.
        Raises an exception if the refresh fails.
    """
    client_id = os.environ.get("AWS_COGNITO_CLIENT_ID")
    if not client_id:
        raise ValueError("AWS_COGNITO_CLIENT_ID environment variable not set.")

    client = boto3.client("cognito-idp")

    try:
        response = client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token
            },
            ClientId=client_id,
        )

        # The response structure might vary based on the Cognito setup.
        # This example assumes a common structure for access and ID tokens.
        new_tokens = {
            "AccessToken": response["AuthenticationResult"]["AccessToken"],
            "IdToken": response["AuthenticationResult"]["IdToken"],
        }
        if "RefreshToken" in response["AuthenticationResult"]:
            new_tokens["RefreshToken"] = response["AuthenticationResult"]["RefreshToken"]
        
        return new_tokens

    except client.exceptions.ClientError as e:
        raise RuntimeError(f"AWS Cognito error during token refresh: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
