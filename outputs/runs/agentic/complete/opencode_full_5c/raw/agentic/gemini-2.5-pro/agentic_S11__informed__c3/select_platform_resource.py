from vertexai.generative_models import GenerativeModel
from model_client import get_client


def select_model(model_name: str) -> GenerativeModel:
    """
    Resolves and returns a provider-specific model resource.

    Args:
        model_name: The name of the model to select (e.g., "gemini-1.5-pro-preview-0409").

    Returns:
        A GenerativeModel instance from the Vertex AI SDK.
    """
    get_client()
    model = GenerativeModel(model_name)
    return model
