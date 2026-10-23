from __future__ import annotations

from typing import Dict, Any

from model_client import bedrock_runtime_client, build_converse_input, load_platform_config
from model_models import PlatformRequest, PlatformResponse


def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    config = load_platform_config()
    client = bedrock_runtime_client(config["aws_region"])
    response = client.converse(**build_converse_input(request))
    platform_response = PlatformResponse(
        text=response["output"]["message"]["content"][0].get("text", ""),
        usage=response.get("usage", {}),
        resource_id=response.get("ResponseMetadata", {}).get("RequestId"),
        model_id=response.get("modelId", request.model),
        raw=response,
    )
    return {
        "text": platform_response.text,
        "usage": platform_response.usage,
        "resource_id": platform_response.resource_id,
        "model_id": platform_response.model_id,
        "raw": platform_response.raw,
    }
