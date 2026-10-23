import os
from urllib import request


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_BEDROCK_MODEL_ID = os.getenv("AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")


def build_bedrock_runtime_client():
    import boto3
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)


def invoke_bedrock_json(payload):
    client = build_bedrock_runtime_client()
    body = client.invoke_model(
        modelId=AWS_BEDROCK_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=payload.encode("utf-8"),
    )["body"].read().decode("utf-8")
    return body


def provider_header():
    return {"x-provider": "aws-bedrock"}
