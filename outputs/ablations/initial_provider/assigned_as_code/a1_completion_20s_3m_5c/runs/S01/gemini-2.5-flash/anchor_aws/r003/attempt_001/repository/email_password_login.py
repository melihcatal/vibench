import base64
import hashlib
import hmac
import os

from identity_client import get_cognito_client
from identity_models import AuthTokens


def email_password_login(payload, config=None) -> AuthTokens:
    config = config or {}
    client = get_cognito_client(config)
    
    client_id = config.get("client_id", os.environ.get("COGNITO_CLIENT_ID"))
    client_secret = config.get("client_secret", os.environ.get("COGNITO_CLIENT_SECRET"))
    
    if not client_id:
        raise ValueError("Cognito Client ID must be provided in config or COGNITO_CLIENT_ID environment variable.")

    request = {
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": client_id,
        "AuthParameters": {
            "USERNAME": payload["email"],
            "PASSWORD": payload["password"],
        }
    }

    if client_secret:
        message = payload["email"] + client_id
        digest = hmac.new(client_secret.encode(), message.encode(), hashlib.sha256).digest()
        request["AuthParameters"]["SECRET_HASH"] = base64.b64encode(digest).decode()
    
    response = client.initiate_auth(**request)
    
    auth_result = response["AuthenticationResult"]
    return AuthTokens(
        access_token=auth_result["AccessToken"],
        refresh_token=auth_result.get("RefreshToken"),
        id_token=auth_result.get("IdToken"),
        expires_in=auth_result.get("ExpiresIn"),
        token_type=auth_result.get("TokenType"),
    )
