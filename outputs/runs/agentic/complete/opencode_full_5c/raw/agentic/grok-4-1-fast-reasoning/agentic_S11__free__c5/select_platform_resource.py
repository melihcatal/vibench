from model_client import get_platform_client
from model_models import ChatMessage
from typing import List


def select_platform_resource(model_hint: str = "gpt-4o") -> str:
    """
    Resolves a provider-specific deployment ID for the given model hint.
    """
    client = get_platform_client()
    available_models = client.models.list(limit=100)
    for model in available_models.data:
        if model_hint.lower() in model.id.lower():
            return model.id
    raise ValueError(f"No matching deployment found for model hint: {model_hint}")
