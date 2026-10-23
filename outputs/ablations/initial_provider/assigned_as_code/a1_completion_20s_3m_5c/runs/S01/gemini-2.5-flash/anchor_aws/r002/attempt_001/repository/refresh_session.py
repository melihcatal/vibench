import os
from identity_client import get_cognito_client

def refresh_session(payload, config=None):
    config = config or {}
    client = get_cognito_client()
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    refresh_token = payload["refresh_token"]

    auth_params = {"REFRESH_TOKEN": refresh_token}

    client_secret = os.environ.get("COGNITO_CLIENT_SECRET")
    if client_secret:
        username = payload.get("username", "") # Username might be needed for SECRET_HASH if refresh token is revoked
        message = username + client_id
        import base64
        import hashlib
        import hmac
        digest = hmac.new(client_secret.encode(), message.encode(), hashlib.sha256).digest()
        auth_params["SECRET_HASH"] = base64.b64encode(digest).decode()

    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters=auth_params,
    )

    return {
        "access_token": response["AuthenticationResult"]["AccessToken"],
        "id_token": response["AuthenticationResult"]["IdToken"],
        "expires_in": response["AuthenticationResult"]["ExpiresIn"],
    }
