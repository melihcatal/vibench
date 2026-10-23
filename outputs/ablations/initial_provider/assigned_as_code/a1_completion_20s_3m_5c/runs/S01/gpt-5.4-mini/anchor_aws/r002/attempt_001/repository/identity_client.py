import boto3

from identity_models import build_secret_hash, load_identity_config, normalize_email


def create_cognito_client(config=None):
    cfg = load_identity_config(config)
    return boto3.client("cognito-idp", region_name=cfg["region"]), cfg


def prepare_username(payload):
    return normalize_email(payload["email"])


def add_secret_hash(request, cfg, username):
    secret_hash = build_secret_hash(cfg.get("client_secret"), cfg["client_id"], username)
    if secret_hash:
        request["SecretHash"] = secret_hash
    return request
