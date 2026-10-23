from model_client import get_cohere_client

# A list of some available Cohere models for demonstration.
# In a real scenario, this might involve an API call to list available resources.
AVAILABLE_MODELS = [
    "command-r",
    "command-r-plus",
    "command",
    "command-light",
    "embed-english-v3.0",
    "embed-multilingual-v3.0",
]


def select_platform_resource(model_name: str) -> str:
    """
    Resolves a provider-specific model resource.
    For Cohere, the model is identified by a string name.
    This function validates if the model is in a known list of models.
    """
    co = get_cohere_client()  # Client initialization demonstrates provider specificity
    if model_name in AVAILABLE_MODELS:
        return model_name
    else:
        raise ValueError(f"Model '{model_name}' is not a known Cohere model.")
