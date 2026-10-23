import os
import base64
import hashlib
import hmac

from identity_client import get_cognito_client


def password_reset(payload, config=None):
    config = config or {}
    client = get_cognito_client(config)
    
    client_id = config.get("client_id", os.environ.get("COGNITO_CLIENT_ID"))
    client_secret = config.get("client_secret", os.environ.get("COGNITO_CLIENT_SECRET"))

    if not client_id:
        raise ValueError("Cognito Client ID must be provided in config or COGNITO_CLIENT_ID environment variable.")

    request = {
        "ClientId": client_id,
        "Username": payload["email"],
    }

    if client_secret:
        message = payload["email"] + client_id
        digest = hmac.new(client_secret.encode(), message.encode(), hashlib.sha256).digest()
        request["SecretHash"] = base64.b64encode(digest).decode()

    client.forgot_password(**request)
    
    return {"status": "password_reset_initiated", "email": payload["email"]}
