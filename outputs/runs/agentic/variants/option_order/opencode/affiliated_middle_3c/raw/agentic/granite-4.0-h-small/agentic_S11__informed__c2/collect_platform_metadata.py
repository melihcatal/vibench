import os
from model_client import ManagedModelClient
from model_models import InferenceRequest, InferenceResponse


def collect_metadata(
    provider: str, responses: list[InferenceResponse], config: dict
) -> dict:
    """Combine raw model output with platform metadata (usage, request ID, handle, etc.). Returns a dict."""
    client = ManagedModelClient(config)
    metadata = {}
    if provider == "huggingface":
        # Example metadata from HF API response: usage quota, request ID
        metadata = {
            "provider": "huggingface",
            "usage": config.get("hf_usage", {}),
            "request_id": responses[0].raw.get("request_id"),
        }
    elif provider == "bedrock":
        metadata = {
            "provider": "bedrock",
            "usage": {"characters": config.get("bedrock_chars_used", 0)},
            "resource_id": client.deployment_id,
        }
    elif provider == "watsonx":
        metadata = {
            "provider": "watsonx",
            "usage": config.get("watsonx_usage", {}),
            "model_handle": client.model_id,
        }
    else:
        metadata = {"provider": provider, "usage": {}, "resource_id": None}
    metadata["raw_outputs"] = [resp.raw for resp in responses]
    return metadata
