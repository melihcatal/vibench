import json
from model_client import ManagedModelClient
from model_models import PlatformMetadata


def platform_output_safety(provider_output: dict, metadata: PlatformMetadata) -> dict:
    """Screen model output for unsafe content using the platform's moderation service.

    Returns a dict with keys "clean" (bool) and "filtered_output" (str) and the original platform metadata.
    """
    # Placeholder: assume the provider returns a moderation verdict under metadata.moderation
    safe = metadata.get("moderation", {}).get("safe", False)
    return {
        "clean": safe,
        "filtered_output": metadata.get("filtered_output", provider_output),
        "metadata": metadata,
    }
