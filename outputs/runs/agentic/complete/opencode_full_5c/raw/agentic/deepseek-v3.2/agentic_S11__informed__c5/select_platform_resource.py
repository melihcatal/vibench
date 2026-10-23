import os
from typing import Dict, List, Optional
from openai import AzureOpenAI
from model_client import get_azure_client


def list_available_models() -> List[Dict[str, str]]:
    """
    List available Azure OpenAI models/deployments.
    """
    client = get_azure_client()

    try:
        deployments = client.deployments.list()

        models = []
        for deployment in deployments:
            models.append(
                {
                    "id": deployment.id,
                    "model": deployment.model,
                    "status": deployment.status,
                    "created_at": deployment.created_at,
                }
            )

        return models
    except Exception as e:
        raise RuntimeError(f"Failed to list Azure OpenAI deployments: {e}")


def resolve_model_resource(model_name: Optional[str] = None) -> str:
    """
    Resolve a specific Azure OpenAI model/deployment for invocation.
    """
    if model_name:
        return model_name

    available_models = list_available_models()

    if not available_models:
        raise ValueError("No Azure OpenAI deployments found")

    gpt4_models = [m for m in available_models if "gpt-4" in m["model"].lower()]
    if gpt4_models:
        return gpt4_models[0]["id"]

    return available_models[0]["id"]


def get_model_capabilities(model_id: str) -> Dict:
    """
    Get capabilities of a specific Azure OpenAI model.
    """
    client = get_azure_client()

    try:
        deployment = client.deployments.retrieve(model_id)

        return {
            "model": deployment.model,
            "max_tokens": 8192 if "gpt-4" in deployment.model.lower() else 4096,
            "supports_chat": True,
            "supports_completion": True,
            "supports_embeddings": "embedding" in deployment.model.lower(),
            "status": deployment.status,
        }
    except Exception as e:
        raise RuntimeError(
            f"Failed to retrieve Azure OpenAI deployment {model_id}: {e}"
        )
