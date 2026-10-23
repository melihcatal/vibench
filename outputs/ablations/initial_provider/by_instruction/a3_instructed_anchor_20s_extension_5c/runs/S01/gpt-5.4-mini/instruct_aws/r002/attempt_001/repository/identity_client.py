import os
from typing import Optional

import boto3


def identity_region() -> str:
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"


def identity_user_pool_id() -> str:
    return os.environ["COGNITO_USER_POOL_ID"]


def identity_client_id() -> str:
    return os.environ["COGNITO_APP_CLIENT_ID"]


def cognito_idp_client(region: Optional[str] = None):
    return boto3.client("cognito-idp", region_name=region or identity_region())


def translate_client(region: Optional[str] = None):
    return boto3.client("translate", region_name=region or identity_region())


def comprehend_client(region: Optional[str] = None):
    return boto3.client("comprehend", region_name=region or identity_region())


def sns_client(region: Optional[str] = None):
    return boto3.client("sns", region_name=region or identity_region())


def dynamodb_resource(region: Optional[str] = None):
    return boto3.resource("dynamodb", region_name=region or identity_region())
