from typing import Dict, Any, Tuple

from .model_models import ChatResponse


def collect_platform_metadata(
    response: ChatResponse,
    deployment_name: str,
    endpoint: str,
    raw_response: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Returns Azure AI Inference model output together with platform metadata.
    Includes usage, model handles, and resource IDs.
    """
    metadata = {
        "model_output": response.content,
        "usage": response.usage,
        "model": response.model,
        "deployment_name": deployment_name,
        "endpoint": endpoint,
        "provider": "azure_ai_inference",
        "raw_response": {
            "id": raw_response.get("id"),
            "created": raw_response.get("created"),
            "system_fingerprint": raw_response.get("system_fingerprint"),
        },
    }

    return metadata
