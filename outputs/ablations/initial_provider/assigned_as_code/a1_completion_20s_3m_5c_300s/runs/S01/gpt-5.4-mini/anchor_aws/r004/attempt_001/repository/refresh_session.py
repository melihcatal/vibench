import boto3

from identity_client import ensure_identity_config, secret_hash
from identity_models import build_cognito_username, extract_tokens


def refresh_session(payload, config=None):
    config = ensure_identity_config(config, required=("client_id",))
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    username = build_cognito_username(payload)
    request = {
        "AuthFlow": "REFRESH_TOKEN_AUTH",
        "ClientId": config["client_id"],
        "AuthParameters": {"REFRESH_TOKEN": payload["refresh_token"]},
    }
    if username:
        request["AuthParameters"]["USERNAME"] = username
    sh = secret_hash(username or payload.get("refresh_token", ""), config["client_id"], config.get("client_secret"))
    if sh:
        request["AuthParameters"]["SECRET_HASH"] = sh
    response = client.initiate_auth(**request)
    return extract_tokens(response)
