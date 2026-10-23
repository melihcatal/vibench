import os


def load_identity_config(config=None):
    config = dict(config or {})
    if "region" not in config:
        config["region"] = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if "user_pool_id" not in config:
        config["user_pool_id"] = os.environ.get("COGNITO_USER_POOL_ID")
    if "client_id" not in config:
        config["client_id"] = os.environ.get("COGNITO_CLIENT_ID")
    if "client_secret" not in config:
        config["client_secret"] = os.environ.get("COGNITO_CLIENT_SECRET")
    return config


def ensure_identity_config(config, required=()):
    config = load_identity_config(config)
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise ValueError("missing configuration: " + ", ".join(missing))
    return config


def cognito_client(region=None):
    import boto3

    return boto3.client("cognito-idp", region_name=region)


def secret_hash(username, client_id, client_secret):
    import base64
    import hashlib
    import hmac

    if not client_secret:
        return None
    digest = hmac.new(client_secret.encode(), (username + client_id).encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()
