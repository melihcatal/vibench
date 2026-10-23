from typing import Optional, Dict, Any
import os
from model_client import get_model_client_config


def select_platform_resource(
    model_identifier: Optional[str] = None,
    deployment_identifier: Optional[str] = None,
    inference_profile: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resolves Azure AI Inference deployment and model resources.
    Returns provider-specific resource identifiers and configuration.
    Uses "gpt-4o" as the concrete model identifier.
    """
    config = get_model_client_config()

    deployment_name = deployment_identifier or config.get(
        "AZURE_AI_INFERENCE_DEPLOYMENT", "gpt-4o"
    )
    endpoint = config.get("AZURE_AI_INFERENCE_ENDPOINT")
    api_key = config.get("AZURE_AI_INFERENCE_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure AI Inference endpoint and API key are required.")

    return {
        "model_identifier": model_identifier or "gpt-4o",
        "deployment_name": deployment_name,
        "endpoint": endpoint,
        "api_key": api_key,
        "inference_profile": inference_profile,
    }
