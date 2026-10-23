import os

import boto3


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")


def build_textract_client(config=None):
    return boto3.client("textract", region_name=get_region(config))


def build_dynamodb_resource(config=None):
    return boto3.resource("dynamodb", region_name=get_region(config))


def document_bytes(payload):
    return payload.get("document_bytes")


def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()
