from typing import Optional, Dict, Any
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from model_client import get_model_client_config


def select_platform_resource(
    model_identifier: Optional[str] = None,
    deployment_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resolves Azure AI Inference deployment and model resources.
    Returns deployment_name, model_identifier, and endpoint.
    """
    config = get_model_client_config()
    deployment_name = deployment_name or config.get(
        "AZURE_AI_INFERENCE_DEPLOYMENT_NAME"
    )
    model_identifier = model_identifier or config.get(
        "AZURE_AI_INFERENCE_MODEL_ID", "gpt-4o"
    )
    endpoint = config.get("AZURE_AI_INFERENCE_ENDPOINT")
    api_key = config.get("AZURE_AI_INFERENCE_KEY")

    if not all([deployment_name, endpoint, api_key]):
        raise ValueError("Missing required Azure AI Inference configuration.")

    return {
        "deployment_name": deployment_name,
        "model_identifier": model_identifier,
        "endpoint": endpoint,
        "api_key": api_key,
    }
