from typing import List
from model_client import get_platform_client

def select_platform_resource(model_hint: str = "gpt-4o") -> str:
    """
    Resolves a provider-specific deployment name for the given model hint.
    """
    client = get_platform_client()
    models = client.models.list()
    for model in models.data:
        if model_hint.lower() in model.id.lower():
            return model.id
    raise ValueError(f"No matching deployment found for model hint: {model_hint}")
