import os

import boto3


def load_identity_config(config=None):
    merged = dict(config or {})
    if "region" not in merged:
        merged["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if "client_id" not in merged:
        merged["client_id"] = os.getenv("COGNITO_CLIENT_ID")
    if "client_secret" not in merged:
        merged["client_secret"] = os.getenv("COGNITO_CLIENT_SECRET")
    if "user_pool_id" not in merged:
        merged["user_pool_id"] = os.getenv("COGNITO_USER_POOL_ID")
    return merged


def cognito_client(config=None):
    loaded = load_identity_config(config)
    return boto3.client("cognito-idp", region_name=loaded.get("region")), loaded
