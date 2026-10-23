from typing import Dict, Any, Tuple
from model_models import ChatResponse
from invoke_platform_model import invoke_platform_model
from select_platform_resource import select_platform_resource


def collect_platform_metadata(
    request: Dict[str, Any],
) -> Tuple[ChatResponse, Dict[str, Any]]:
    """
    Invokes Azure AI Inference model and returns output with platform metadata.
    Metadata includes usage, resource IDs, and model handles.
    """
    resource_config = select_platform_resource()
    chat_request = ChatRequest(
        system_prompt=request.get("system_prompt"),
        messages=request.get("messages", []),
    )

    response = invoke_platform_model(
        request=chat_request,
        deployment_name=resource_config["deployment_name"],
        endpoint=resource_config["endpoint"],
        api_key=resource_config["api_key"],
    )

    metadata = {
        "model_identifier": resource_config["model_identifier"],
        "deployment_name": resource_config["deployment_name"],
        "usage": response.raw_response.get("usage", {}),
        "system_fingerprint": response.raw_response.get("system_fingerprint"),
    }

    return response, metadata
