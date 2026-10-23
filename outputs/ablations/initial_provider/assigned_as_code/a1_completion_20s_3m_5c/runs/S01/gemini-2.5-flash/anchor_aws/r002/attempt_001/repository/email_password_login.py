import os
import base64
import hashlib
import hmac
from identity_client import get_cognito_client

def email_password_login(payload, config=None):
    config = config or {}
    client = get_cognito_client()
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    username = payload["email"]
    password = payload["password"]

    auth_params = {"USERNAME": username, "PASSWORD": password}

    client_secret = os.environ.get("COGNITO_CLIENT_SECRET")
    if client_secret:
        message = username + client_id
        digest = hmac.new(client_secret.encode(), message.encode(), hashlib.sha256).digest()
        auth_params["SECRET_HASH"] = base64.b64encode(digest).decode()

    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters=auth_params,
    )
    return {
        "access_token": response["AuthenticationResult"]["AccessToken"],
        "refresh_token": response["AuthenticationResult"]["RefreshToken"],
        "id_token": response["AuthenticationResult"]["IdToken"],
        "expires_in": response["AuthenticationResult"]["ExpiresIn"],
    }
