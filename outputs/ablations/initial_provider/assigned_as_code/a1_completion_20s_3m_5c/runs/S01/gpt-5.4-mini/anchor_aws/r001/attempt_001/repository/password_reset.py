import boto3

from identity_client import load_identity_config, secret_hash
from identity_models import normalize_email_password_payload


def password_reset(payload, config=None):
    payload = normalize_email_password_payload(payload)
    config = load_identity_config(config)
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    request = {"ClientId": config["client_id"], "Username": payload["email"]}
    if config.get("client_secret"):
        request["SecretHash"] = secret_hash(payload["email"], config["client_id"], config["client_secret"])
    client.forgot_password(**request)
    return {"status": "reset_started", "email": payload["email"]}
