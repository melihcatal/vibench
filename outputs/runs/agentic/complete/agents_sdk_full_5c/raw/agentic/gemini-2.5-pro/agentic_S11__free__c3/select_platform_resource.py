import os
from typing import List, Optional
import cohere

def list_available_models() -> List[str]:
    """Returns a list of available model names from Cohere."""
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))
    models = client.models.list()
    return [model.name for model in models]

def resolve_model_resource(model_name_prefix: str) -> Optional[str]:
    """
    Resolves a model resource by finding a model with the given prefix.
    
    Args:
        model_name_prefix: The prefix to search for (e.g., "command").
        
    Returns:
        The full model name if found, otherwise None.
    """
    available_models = list_available_models()
    for model_name in available_models:
        if model_name.startswith(model_name_prefix):
            return model_name
    return None

def select_command_r_plus() -> Optional[str]:
    """Selects the Command R+ model."""
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))
    models = client.models.list()
    # A more specific way to find the model resource
    for model in models:
        if model.name == "command-r-plus" and "chat" in model.endpoints:
            return model.name
    return None
