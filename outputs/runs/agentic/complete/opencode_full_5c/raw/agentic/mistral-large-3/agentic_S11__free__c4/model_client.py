import os
from typing import Dict, Any, Optional

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential


def get_model_client_config() -> Dict[str, str]:
    """
    Loads Azure AI Inference client configuration from environment variables.
    """
    return {
        "AZURE_AI_ENDPOINT": os.getenv("AZURE_AI_ENDPOINT"),
        "AZURE_AI_API_KEY": os.getenv("AZURE_AI_API_KEY"),
        "AZURE_AI_DEPLOYMENT_NAME": os.getenv("AZURE_AI_DEPLOYMENT_NAME"),
    }


def get_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ChatCompletionsClient:
    """
    Initializes and returns an Azure AI Inference client.
    """
    config = get_model_client_config()

    endpoint = endpoint or config.get("AZURE_AI_ENDPOINT")
    api_key = api_key or config.get("AZURE_AI_API_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure AI endpoint and API key must be provided.")

    return ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )
