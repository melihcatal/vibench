import boto3

from identity_client import ensure_identity_config, secret_hash
from identity_models import build_cognito_username, extract_tokens


def email_password_login(payload, config=None):
    config = ensure_identity_config(config, required=("client_id",))
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    username = build_cognito_username(payload)
    request = {
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": config["client_id"],
        "AuthParameters": {"USERNAME": username, "PASSWORD": payload["password"]},
    }
    sh = secret_hash(username, config["client_id"], config.get("client_secret"))
    if sh:
        request["AuthParameters"]["SECRET_HASH"] = sh
    response = client.initiate_auth(**request)
    return extract_tokens(response)
