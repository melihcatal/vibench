from model_client import get_cohere_client

# A list of known, valid Cohere model identifiers for this application
KNOWN_COHERE_MODELS = [
    "command-r",
    "command-r-plus",
    "command",
    "command-light",
]

def select_model_resource(model_name: str) -> str:
    """
    Resolves a provider-specific model resource before invocation.

    In the Cohere SDK, the model resource is identified by its string name.
    This function validates that the requested model is a known, supported
    generation model for this application.

    Args:
        model_name: The identifier of the model to use (e.g., "command-r").

    Returns:
        The validated model name.
        
    Raises:
        ValueError: If the model_name is not in the known list.
    """
    # This check represents the selection logic.
    if model_name in KNOWN_COHERE_MODELS:
        # With Cohere, the model ID string is the resource handle.
        # This function confirms its validity before use.
        # A more complex version could query a model management API.
        get_cohere_client() # Implicitly validates API key is present
        return model_name
    else:
        raise ValueError(f"Model '{model_name}' is not a known Cohere resource.")
