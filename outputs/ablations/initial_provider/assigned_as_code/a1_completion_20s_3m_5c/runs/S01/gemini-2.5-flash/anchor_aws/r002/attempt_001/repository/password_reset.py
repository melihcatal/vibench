import os
import base64
import hashlib
import hmac
from identity_client import get_cognito_client

def password_reset(payload, config=None):
    config = config or {}
    client = get_cognito_client()
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    username = payload["email"]

    client_secret = os.environ.get("COGNITO_CLIENT_SECRET")
    if client_secret:
        message = username + client_id
        digest = hmac.new(client_secret.encode(), message.encode(), hashlib.sha256).digest()
        secret_hash = base64.b64encode(digest).decode()
        response = client.forgot_password(
            ClientId=client_id,
            Username=username,
            SecretHash=secret_hash
        )
    else:
        response = client.forgot_password(
            ClientId=client_id,
            Username=username
        )

    return {"status": response["CodeDeliveryDetails"]["DeliveryMedium"]}
