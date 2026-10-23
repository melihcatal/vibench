import os

import boto3


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")


def get_secrets_manager_client(config=None):
    return boto3.client("secretsmanager", region_name=get_region(config))


def get_default_stage(config=None):
    config = config or {}
    return config.get("version_stage") or os.getenv("SECRET_VERSION_STAGE") or "AWSCURRENT"
