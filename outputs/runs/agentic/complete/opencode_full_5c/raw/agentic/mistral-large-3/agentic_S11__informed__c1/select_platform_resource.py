from typing import Optional, Dict, Any
import os
from openai import AzureOpenAI


def select_platform_resource(
    model_name: Optional[str] = None, deployment_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Resolves an Azure OpenAI deployment or model resource for invocation.
    Returns the deployment name and model identifier for the selected resource.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
    )

    if not deployment_name:
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        if not deployment_name:
            raise ValueError(
                "Deployment name must be provided or set in AZURE_OPENAI_DEPLOYMENT_NAME."
            )

    if not model_name:
        model_name = "gpt-4o"

    return {
        "deployment_name": deployment_name,
        "model_name": model_name,
        "api_version": "2024-02-01",
        "provider": "azure_openai",
    }
