import cohere

# A curated list of known compatible Cohere models for this workflow
KNOWN_COHERE_MODELS = {
    "command-r",
    "command-r-plus",
    "command",
    "command-light",
}

def resolve_cohere_model(model_name: str) -> str:
    """
    Resolves and validates a Cohere model identifier.

    Args:
        model_name: The name of the model to resolve.

    Returns:
        The validated model name.

    Raises:
        ValueError: If the model_name is not a known Cohere model.
    """
    if model_name in KNOWN_COHERE_MODELS:
        return model_name
    else:
        raise ValueError(f"Model '{model_name}' is not a known Cohere model.")
