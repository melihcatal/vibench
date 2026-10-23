import os
import base64
from typing import Optional
from identity_client import CognitoClient
from identity_models import OAuthTokens

def exchange_code_for_tokens(code: str) -> OAuthTokens:
    cognito_client = CognitoClient()
    if not cognito_client.client_id or not cognito_client.redirect_uri:
        raise ValueError("Missing Cognito configuration environment variables.")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    if cognito_client.client_secret:
        secret_bytes = f"{cognito_client.client_id}:{cognito_client.client_secret}".encode("utf-8")
        encoded_secret = base64.b64encode(secret_bytes).decode("utf-8")
        headers["Authorization"] = f"Basic {encoded_secret}"

    try:
        response = cognito_client.cognito_client.token(
            grant_type="authorization_code",
            client_id=cognito_client.client_id,
            code=code,
            redirect_uri=cognito_client.redirect_uri,
            client_secret=cognito_client.client_secret if cognito_client.client_secret else None
        )

        return OAuthTokens(
            access_token=response["access_token"],
            id_token=response.get("id_token"),
            refresh_token=response.get("refresh_token"),
            expires_in=response.get("expires_in"),
            token_type=response.get("token_type", "Bearer")
        )
    except cognito_client.cognito_client.exceptions.ClientError as e:
        raise RuntimeError(f"Failed to exchange code for tokens: {e}")
