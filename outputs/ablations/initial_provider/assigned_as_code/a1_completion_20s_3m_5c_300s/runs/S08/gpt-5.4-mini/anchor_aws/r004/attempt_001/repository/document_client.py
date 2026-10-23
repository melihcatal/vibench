import os

import boto3


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")


def textract_client(config=None):
    return boto3.client("textract", region_name=get_region(config))


def bedrock_runtime_client(config=None):
    return boto3.client("bedrock-runtime", region_name=get_region(config))


def ddb_resource(config=None):
    return boto3.resource("dynamodb", region_name=get_region(config))
