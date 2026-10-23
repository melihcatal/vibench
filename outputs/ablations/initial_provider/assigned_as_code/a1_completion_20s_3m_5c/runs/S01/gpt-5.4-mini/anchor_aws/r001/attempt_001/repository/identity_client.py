import base64
import hashlib
import hmac
import os

import boto3


def load_identity_config(config=None):
    config = dict(config or {})
    config.setdefault("region", os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    config.setdefault("client_id", os.getenv("COGNITO_CLIENT_ID"))
    config.setdefault("client_secret", os.getenv("COGNITO_CLIENT_SECRET"))
    config.setdefault("user_pool_id", os.getenv("COGNITO_USER_POOL_ID"))
    return config


def cognito_client(config=None):
    config = load_identity_config(config)
    return boto3.client("cognito-idp", region_name=config.get("region"))


def secret_hash(username, client_id, client_secret):
    if not client_secret:
        return None
    digest = hmac.new(client_secret.encode(), (username + client_id).encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def build_auth_params(payload, config=None):
    config = load_identity_config(config)
    username = payload.get("email") or payload.get("username")
    params = {"USERNAME": username, "PASSWORD": payload["password"]}
    if config.get("client_secret"):
        params["SECRET_HASH"] = secret_hash(username, config["client_id"], config["client_secret"])
    return params


def normalize_email(value):
    return value.strip().lower() if isinstance(value, str) else value
