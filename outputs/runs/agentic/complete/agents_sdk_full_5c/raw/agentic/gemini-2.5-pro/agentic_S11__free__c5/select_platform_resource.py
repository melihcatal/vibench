from vertexai.generative_models import GenerativeModel
from model_client import get_vertex_client

def get_model(model_name: str = "gemini-1.5-flash-001") -> GenerativeModel:
    """
    Resolves and returns a provider-specific model resource.

    Args:
        model_name: The identifier of the model to use.

    Returns:
        An initialized GenerativeModel client for the specified model.
    """
    get_vertex_client()  # Ensures the vertexai client is initialized
    model = GenerativeModel(model_name)
    return model

