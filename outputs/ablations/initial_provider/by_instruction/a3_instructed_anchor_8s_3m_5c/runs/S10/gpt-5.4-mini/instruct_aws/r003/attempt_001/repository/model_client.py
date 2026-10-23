import os
from functools import lru_cache

import boto3


def _env(name, default=None):
    value = os.getenv(name)
    return default if value is None or value == "" else value


def get_region():
    return _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1"))


@lru_cache(maxsize=1)
def bedrock_runtime_client():
    return boto3.client("bedrock-runtime", region_name=get_region())


def model_id(name=None):
    mapping = {
        "summarize": _env("BEDROCK_SUMMARIZE_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        "extract": _env("BEDROCK_EXTRACT_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        "answer": _env("BEDROCK_ANSWER_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        "stream": _env("BEDROCK_STREAM_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        "safety": _env("BEDROCK_SAFETY_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        "translate": _env("BEDROCK_TRANSLATE_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        "embed": _env("BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v2:0"),
        "spoken": _env("BEDROCK_SPOKEN_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
    }
    return mapping.get(name or "summarize", mapping["summarize"])


def invoke_bedrock(model, payload):
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model,
        body=payload.encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return response["body"].read().decode("utf-8")


def stream_bedrock(model, payload):
    client = bedrock_runtime_client()
    response = client.invoke_model_with_response_stream(
        modelId=model,
        body=payload.encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    for event in response["body"]:
        yield event
