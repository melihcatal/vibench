import os
from typing import Any, Dict

import boto3


def aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def sns_client():
    return boto3.client("sns", region_name=aws_region())


def sqs_client():
    return boto3.client("sqs", region_name=aws_region())


def comprehend_client():
    return boto3.client("comprehend", region_name=aws_region())


def translate_client():
    return boto3.client("translate", region_name=aws_region())


def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=aws_region())


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def client_metadata(client: Any) -> Dict[str, Any]:
    return {"service": getattr(client.meta, "service_model", None).service_name if getattr(client, "meta", None) else ""}
