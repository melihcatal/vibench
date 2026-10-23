from typing import Optional, Dict, Any
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from .model_client import get_model_client_config


def select_platform_resource(
    model_identifier: Optional[str] = None,
    deployment_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resolves an Azure AI Inference deployment or model resource.
    Returns the deployment name, endpoint, and API key.
    """
    config = get_model_client_config()
    deployment_name = deployment_name or config.get(
        "AZURE_AI_INFERENCE_DEPLOYMENT_NAME"
    )
    endpoint = config.get("AZURE_AI_INFERENCE_ENDPOINT")
    api_key = config.get("AZURE_AI_INFERENCE_KEY")

    if not all([deployment_name, endpoint, api_key]):
        raise ValueError("Missing required configuration for Azure AI Inference.")

    # Verify the deployment is accessible
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )
    try:
        # Test the deployment with a minimal request
        client.complete(
            messages=[{"role": "user", "content": "Hello"}],
            model_extras={"model": deployment_name, "max_tokens": 1},
        )
    except Exception as e:
        raise ValueError(f"Failed to verify Azure AI Inference deployment: {e}")

    return {
        "deployment_name": deployment_name,
        "endpoint": endpoint,
        "api_key": api_key,
        "model_identifier": deployment_name,
    }
