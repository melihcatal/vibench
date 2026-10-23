import os
from model_client import get_platform_config

def select_platform_resource(resource_type: str = "chat") -> str:
    """
    Resolve provider-specific model deployment for Azure OpenAI.
    """
    config = get_platform_config()
    # Azure OpenAI deployment names
    deployments = {
        "chat": "gpt-4o",
        "reasoning": "o1-preview",
        "completion": "gpt-4o-mini",
        "embedding": "text-embedding-3-large"
    }
    return deployments.get(resource_type, config["deployment"])