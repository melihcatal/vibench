from __future__ import annotations

from typing import Any, Dict

from model_client import bedrock_runtime_client, build_converse_input, load_platform_config
from model_models import PlatformRequest, PlatformResponse


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    config = load_platform_config()
    client = bedrock_runtime_client(config["aws_region"])
    payload: Dict[str, Any] = build_converse_input(request)
    response = client.converse(**payload)
    return PlatformResponse(
        text=response["output"]["message"]["content"][0].get("text", ""),
        usage=response.get("usage", {}),
        resource_id=response.get("ResponseMetadata", {}).get("RequestId"),
        model_id=response.get("modelId", request.model),
        raw=response,
    )
