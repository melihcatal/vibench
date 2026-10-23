import os

import boto3


def bedrock_converse_client():
    return boto3.client("bedrock-runtime")


def bedrock_runtime_client():
    return boto3.client("bedrock-runtime")


def resolve_platform_resource(model_name: str):
    return {
        "modelId": os.getenv("BEDROCK_MODEL_ID", model_name),
        "provider": "Amazon Bedrock",
    }
