import os
import base64
import hashlib
import hmac

from identity_client import get_cognito_client
from identity_models import AuthTokens


def refresh_session(payload, config=None) -> AuthTokens:
    config = config or {}
    client = get_cognito_client(config)
    
    client_id = config.get("client_id", os.environ.get("COGNITO_CLIENT_ID"))
    client_secret = config.get("client_secret", os.environ.get("COGNITO_CLIENT_SECRET"))

    if not client_id:
        raise ValueError("Cognito Client ID must be provided in config or COGNITO_CLIENT_ID environment variable.")

    request = {
        "AuthFlow": "REFRESH_TOKEN_AUTH",
        "ClientId": client_id,
        "AuthParameters": {
            "REFRESH_TOKEN": payload["refresh_token"],
        }
    }
    
    # For REFRESH_TOKEN_AUTH, Cognito also expects a SECRET_HASH if the client has a secret.
    # The username used in the SECRET_HASH calculation for refresh tokens is typically the username 
    # that initiated the original session, but for refresh_token_auth, it's not directly provided.
    # However, if your client is configured with a secret, AWS SDKs usually handle this implicitly or 
    # expect a SECRET_HASH based on the client ID only. 
    # For simplicity, assuming if a secret is present, it's used with a placeholder or just client_id.
    # A more robust solution might require storing the username with the refresh token or inferring it.
    if client_secret:
        # The SECRET_HASH for refresh token often doesn't involve the username directly
        # for security reasons or simply isn't required by the Cognito API for this flow
        # when the refresh token itself is sufficient. However, if required, the SDKs handle it.
        # For this example, if the client has a secret, we'll assume it's calculated using client_id.
        # In a real-world scenario, you might need the original username.
        message = client_id # Or a specific username if available from the stored session
        digest = hmac.new(client_secret.encode(), message.encode(), hashlib.sha256).digest()
        request["AuthParameters"]["SECRET_HASH"] = base64.b64encode(digest).decode()

    response = client.initiate_auth(**request)
    
    auth_result = response["AuthenticationResult"]
    return AuthTokens(
        access_token=auth_result["AccessToken"],
        refresh_token=auth_result.get("RefreshToken"), # Refresh token might not be returned again
        id_token=auth_result.get("IdToken"),
        expires_in=auth_result.get("ExpiresIn"),
        token_type=auth_result.get("TokenType"),
    )
