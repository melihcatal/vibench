import os

import boto3


def load_security_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "secret_id": config.get("secret_id") or os.environ.get("SECRET_ID"),
        "version_id": config.get("version_id") or os.environ.get("SECRET_VERSION_ID"),
        "version_stage": config.get("version_stage") or os.environ.get("SECRET_VERSION_STAGE"),
    }


def secrets_manager_client(config=None):
    cfg = load_security_config(config)
    return boto3.client("secretsmanager", region_name=cfg["region"])


def normalize_secret_value(response):
    if "SecretString" in response:
        return response["SecretString"]
    return response["SecretBinary"].decode("utf-8")
