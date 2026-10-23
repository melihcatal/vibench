import os
from typing import Any, Dict, Iterable, Iterator, Optional

import boto3

from model_models import PlatformRequest, PlatformResponse, merge_usage, normalize_text


AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")


def get_bedrock_runtime():
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)


def build_invoke_payload(request: PlatformRequest) -> Dict[str, Any]:
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "messages": [{"role": "user", "content": [{"type": "text", "text": request.prompt}]}],
    }


def invoke_bedrock_model(request: PlatformRequest, model_id: Optional[str] = None) -> PlatformResponse:
    client = get_bedrock_runtime()
    target_model = model_id or request.model_id or BEDROCK_MODEL_ID
    response = client.invoke_model(modelId=target_model, body=str(build_invoke_payload(request)).replace("'", '"'))
    body = response["body"].read().decode("utf-8")
    parsed = __import__("json").loads(body)
    text = normalize_text(parsed.get("content", []))
    usage = merge_usage(parsed.get("usage"), {k: response.get(k) for k in ("ResponseMetadata",) if response.get(k)})
    return PlatformResponse(text=text, model_id=target_model, usage=usage, raw=parsed)


def stream_bedrock_model(request: PlatformRequest, model_id: Optional[str] = None) -> Iterator[Any]:
    client = get_bedrock_runtime()
    target_model = model_id or request.model_id or BEDROCK_MODEL_ID
    stream = client.invoke_model_with_response_stream(modelId=target_model, body=str(build_invoke_payload(request)).replace("'", '"'))
    for event in stream["body"]:
        yield event


def select_bedrock_resource(preferred_model: Optional[str] = None) -> str:
    return preferred_model or BEDROCK_MODEL_ID
