import base64
import hashlib
import hmac

import boto3


def register_user(payload, config=None):
    config = config or {}
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    request = {"ClientId": config["client_id"], "Username": payload["email"],
               "Password": payload["password"],
               "UserAttributes": [{"Name": "email", "Value": payload["email"]}]}
    if config.get("client_secret"):
        digest = hmac.new(config["client_secret"].encode(),
                          (payload["email"] + config["client_id"]).encode(), hashlib.sha256).digest()
        request["SecretHash"] = base64.b64encode(digest).decode()
    response = client.sign_up(**request)
    return {"user_id": response["UserSub"]}
