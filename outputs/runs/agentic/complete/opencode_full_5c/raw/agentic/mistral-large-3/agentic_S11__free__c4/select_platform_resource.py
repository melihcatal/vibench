import os
from typing import Optional, Dict, Any

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential


def select_platform_resource(
    model_name: Optional[str] = None,
    deployment_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resolves Azure AI Inference deployment or model resource.
    Returns deployment-specific configuration including endpoint and model details.
    """
    endpoint = os.getenv("AZURE_AI_ENDPOINT")
    api_key = os.getenv("AZURE_AI_API_KEY")
    deployment_name = deployment_name or os.getenv("AZURE_AI_DEPLOYMENT_NAME")

    if not endpoint or not api_key:
        raise ValueError("Azure AI endpoint and API key must be configured.")

    if not deployment_name:
        raise ValueError("Azure AI deployment name must be provided.")

    # Verify deployment accessibility
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )

    return {
        "deployment_name": deployment_name,
        "model_name": model_name or deployment_name,
        "endpoint": endpoint,
        "api_key": api_key,
        "provider": "azure_ai_inference",
    }
