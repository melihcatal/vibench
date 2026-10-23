import os
from huggingface_hub import HfApi


def collect_platform_metadata(response: dict) -> dict:
    """Extract platform metadata from a provider response.
    This generic helper preserves useful fields such as usage, model handle, request ID, etc.
    Returns a cleaned dict with provider-agnostic metadata.
    """
    metadata = {
        "usage": response.get("usage", None),
        "model_handle": response.get("model_handle", None),
        "request_id": response.get("request_id", None),
        "raw": response,  # keep raw payload for further analysis if needed
    }
    return metadata
