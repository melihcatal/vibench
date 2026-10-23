import os

import boto3


def resolve_platform_resource(model_name: str):
    client = boto3.client("bedrock")
    model_id = os.getenv("BEDROCK_MODEL_ID", model_name)
    return {"modelId": model_id, "provider": "amazon-bedrock", "client": client}
