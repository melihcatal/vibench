import os
from typing import Dict, Any
from model_client import get_azure_client


def select_platform_resource(
    model_family: str = None, deployment_type: str = "chat"
) -> Dict[str, Any]:
    """Resolve Azure OpenAI specific model, deployment, or inference resource before invocation."""
    client = get_azure_client()

    # Azure OpenAI specific resource resolution
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    # Determine model based on family or default
    if model_family == "gpt-4":
        model_id = "gpt-4"
        deployment_name = (
            deployment_name if deployment_name.startswith("gpt-4") else "gpt-4o"
        )
    elif model_family == "gpt-3.5":
        model_id = "gpt-3.5-turbo"
        deployment_name = (
            deployment_name
            if deployment_name.startswith("gpt-3.5")
            else "gpt-3.5-turbo"
        )
    else:
        # Default to GPT-4 family
        model_id = "gpt-4o"

    # Azure OpenAI specific deployment configuration
    resource_info = {
        "provider": "azure-openai",
        "endpoint": endpoint,
        "deployment_name": deployment_name,
        "model_id": model_id,
        "deployment_type": deployment_type,
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        "resource_group": os.getenv("AZURE_RESOURCE_GROUP", ""),
        "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID", ""),
    }

    # Validate deployment exists (simplified check)
    try:
        # In real implementation, would check deployments list
        # For now, just return the resolved resource
        return resource_info
    except Exception as e:
        raise ValueError(f"Failed to resolve Azure OpenAI resource: {e}")
